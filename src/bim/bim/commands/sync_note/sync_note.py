import tzlocal

from pathlib import Path
from datetime import datetime
from buvis.pybase.adapters import (
    console,
)
from buvis.pybase.configuration import Configuration, ConfigurationKeyNotFoundError
from doogat.core import (
    MarkdownZettelFormatter,
    MarkdownZettelRepository,
    ReadDoogatUseCase,
)
from doogat.core.domain.entities import ProjectZettel
from doogat.integrations.jira import (
    JiraAdapter,
)

DEFAULT_JIRA_IGNORE_US_LABEL = "do-not-track"


class CommandSyncNote:
    def __init__(self: "CommandSyncNote", cfg: Configuration) -> None:
        try:
            path_note = Path(str(cfg.get_configuration_item("path_note")))
            if not path_note.is_file():
                raise FileNotFoundError
            self.path_note = path_note
        except ConfigurationKeyNotFoundError as e:
            raise FileNotFoundError from e

        match cfg.get_configuration_item("target_system"):
            case "jira":
                jira_cfg = cfg.copy("jira_adapter")
                self._target = JiraAdapter(jira_cfg)
            case _:
                raise NotImplementedError
        self._cfg = cfg

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

        cfg_jira_adapter = self._cfg.get_configuration_item("jira_adapter")

        if isinstance(cfg_jira_adapter, dict):
            cfg_dict_jira_adapter = cfg_jira_adapter.copy()
            ignore_flag = cfg_dict_jira_adapter.get(
                "ignore",
                DEFAULT_JIRA_IGNORE_US_LABEL,
            )
        else:
            ignore_flag = DEFAULT_JIRA_IGNORE_US_LABEL

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
