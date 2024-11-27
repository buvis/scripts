from pathlib import Path

from buvis.pybase.adapters import console, JiraAdapter
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

        defaults = self._cfg.get_configuration_item("jira_adapter")["defaults"]
        if note.type != "project":
            console.failure(f"{self.path_note} is not a project")
            return None

        if not hasattr(note, "us") or not note.us:
            if note.deliverable == "enhancement":
                issue_type = {"name": defaults["enhancements"]["issue_type"]}
                feature = defaults["enhancements"]["feature"]
                labels = defaults["enhancements"]["labels"].split(",")
                priority = {"name": defaults["enhancements"]["priority"]}
            else:
                issue_type = {"name": defaults["bugs"]["issue_type"]}
                feature = defaults["bugs"]["feature"]
                labels = defaults["bugs"]["labels"].split(",")
                priority = {"name": defaults["bugs"]["priority"]}

            description = "No description provided"

            for section in note._data.sections:
                title, content = section
                if title == "## Description":
                    description = content

            new_issue = self._target.create_issue(
                title = note.title,
                description = description,
                feature = feature,
                issue_type = issue_type,
                labels = labels,
                priority = priority,
                ticket = note.ticket,
            )
            note._data.reference["us"] = new_issue.link

            formatted_content = formatter.format(note.get_data())

            self.path_note.write_bytes(formatted_content.encode("utf-8"))
            console.success(f"Jira Issue {new_issue.key} created from {self.path_note}")
        else:
            console.success("No Jira Issue creation necessary")
