import importlib.util
from datetime import datetime
from pathlib import Path
from typing import Any

import tzlocal
from buvis.pybase.adapters import JiraAdapter, console
from doogat.core import (
    MarkdownZettelFormatter,
    MarkdownZettelRepository,
    ReadDoogatUseCase,
)
from doogat.core.domain.entities import ProjectZettel


def _get_assembler_class():
    """Load assembler directly to avoid doogat.integrations.jira.__init__ which needs old Configuration."""
    import doogat

    doogat_path = Path(doogat.__file__).parent
    assembler_path = doogat_path / "integrations" / "jira" / "assemblers" / "project_zettel_jira_issue.py"

    spec = importlib.util.spec_from_file_location("_assembler", assembler_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {assembler_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ProjectZettelJiraIssueDTOAssembler

DEFAULT_JIRA_IGNORE_US_LABEL = "do-not-track"


class DictConfig:
    """Shim providing Configuration-like interface over a dict."""

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    def get_configuration_item(self, key: str) -> Any:
        return self._data[key]

    def get_configuration_item_or_default(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)


class DoogatJiraAdapter(JiraAdapter):
    """JiraAdapter that can create issues from ProjectZettel."""

    def __init__(self, cfg: DictConfig) -> None:
        super().__init__(cfg)
        self._cfg = cfg

    def create_from_project(self, project: ProjectZettel):
        defaults = self._cfg.get_configuration_item("defaults")
        if not isinstance(defaults, dict):
            msg = f"Can't get the defaults from:\n{defaults}"
            raise ValueError(msg)
        assembler_cls = _get_assembler_class()
        assembler = assembler_cls(defaults=defaults.copy())
        dto = assembler.to_dto(project)
        return self.create(dto)


class CommandSyncNote:
    def __init__(
        self: "CommandSyncNote",
        path_note: Path,
        target_system: str,
        jira_adapter_config: dict[str, Any],
    ) -> None:
        if not path_note.is_file():
            raise FileNotFoundError(f"Note not found: {path_note}")
        self.path_note = path_note
        self.jira_adapter_config = jira_adapter_config

        match target_system:
            case "jira":
                jira_cfg = DictConfig(jira_adapter_config)
                self._target = DoogatJiraAdapter(jira_cfg)
            case _:
                raise NotImplementedError(f"Target system '{target_system}' not supported")

    def execute(self: "CommandSyncNote") -> None:
        repo = MarkdownZettelRepository()
        reader = ReadDoogatUseCase(repo)
        formatter = MarkdownZettelFormatter()
        note = reader.execute(str(self.path_note))

        if isinstance(note, ProjectZettel):
            project: ProjectZettel = note
        else:
            console.failure(f"{self.path_note} is not a project")
            return

        ignore_flag = self.jira_adapter_config.get("ignore", DEFAULT_JIRA_IGNORE_US_LABEL)

        if not hasattr(project, "us") or not project.us:
            new_issue = self._target.create_from_project(project)
            md_style_link = f"[{new_issue.id}]({new_issue.link})"
            project.us = md_style_link
            project.add_log_entry(
                f"- [i] {datetime.now(tzlocal.get_localzone()).strftime("%Y-%m-%d %H:%M")} - Jira Issue created: {md_style_link}",
            )
            formatted_content = formatter.format(project.get_data())
            self.path_note.write_bytes(formatted_content.encode("utf-8"))
            console.success(f"Jira Issue {new_issue.id} created from {self.path_note}")
        elif note.us == ignore_flag:
            console.warning("Project is set to ignore Jira")
        else:
            console.success(f"Already linked to {note.us}")
