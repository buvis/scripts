from pathlib import Path
from datetime import datetime
from buvis.pybase.adapters import console, JiraAdapter, ProjectZettelJiraIssueDTOAssembler
from buvis.pybase.configuration import Configuration, ConfigurationKeyNotFoundError
from doogat.core import (
    MarkdownZettelFormatter,
    MarkdownZettelRepository,
    ReadDoogatUseCase,
)


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
                self._target = JiraAdapter(cfg.get_configuration_item("jira_adapter"))
            case _:
                raise NotImplementedError
        self._cfg = cfg

    def execute(self: "CommandSyncNote") -> None:
        repo = MarkdownZettelRepository()
        reader = ReadDoogatUseCase(repo)
        formatter = MarkdownZettelFormatter()
        note = reader.execute(str(self.path_note))

        if note.type != "project":
            console.failure(f"{self.path_note} is not a project")
            return None

        if not hasattr(note, "us") or not note.us:
            assembler = ProjectZettelJiraIssueDTOAssembler(defaults = self._cfg.get_configuration_item("jira_adapter")["defaults"])
            dto = assembler.to_dto(note)
            new_issue = self._target.create(dto)
            md_style_link = f"[{new_issue.id}]({new_issue.link})"
            note._data.reference["us"] = md_style_link
            note.add_log_entry(f"- [i] {datetime.now().strftime("%Y-%m-%d %H:%M")} - Jira Issue created: {md_style_link}")
            formatted_content = formatter.format(note.get_data())
            self.path_note.write_bytes(formatted_content.encode("utf-8"))
            console.success(f"Jira Issue {new_issue.id} created from {self.path_note}")
        elif note.us == self._defaults["ignore"]:
            console.warning("Project is set to ignore Jira")
        else:
            console.success(f"Already linked to {note.us}")
