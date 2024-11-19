from pathlib import Path

from buvis.pybase.adapters import console
from buvis.pybase.configuration import Configuration, ConfigurationKeyNotFoundError
from doogat.core import (
    MarkdownZettelFormatter,
    MarkdownZettelRepository,
    ReadDoogatUseCase,
)


class CommandFormatNote:
    def __init__(self: "CommandFormatNote", cfg: Configuration) -> None:
        try:
            path_note = Path(str(cfg.get_configuration_item("path_note")))
            if not path_note.is_file():
                raise FileNotFoundError
            self.path_note = path_note
        except ConfigurationKeyNotFoundError as e:
            raise FileNotFoundError from e

        self.is_highlighting = cfg.get_configuration_item_or_default(
            "is_highlighting_requested",
            default=False,
        )
        self.is_printing_diff = cfg.get_configuration_item_or_default(
            "is_diff_requested",
            default=False,
        )

        try:
            self.path_output = Path(
                str(cfg.get_configuration_item("path_output")),
            ).resolve()
        except ConfigurationKeyNotFoundError as _:
            self.path_output = None

    def execute(self: "CommandFormatNote") -> None:
        original_content = self.path_note.read_text()
        repo = MarkdownZettelRepository()
        reader = ReadDoogatUseCase(repo)
        formatter = MarkdownZettelFormatter()
        note = reader.execute(str(self.path_note))
        formatted_content = formatter.format(note.get_data())

        if self.path_output:
            try:
                self.path_output.write_text(formatted_content, encoding="UTF-8")
            except OSError as e:
                console.panic(f"An error occurred while writing to the file: {e}")
            except UnicodeEncodeError:
                console.panic("The text could not be encoded with UTF-8")

            console.success(f"Formatted note was written to {self.path_output}")

            return

        if self.is_printing_diff and original_content != formatted_content:
            console.print_side_by_side(
                "Original",
                original_content,
                "Formatted",
                formatted_content,
                mode_left="raw",
                mode_right="markdown_with_frontmatter",
            )
        elif self.is_highlighting:
            console.print(formatted_content, mode="markdown_with_frontmatter")
        else:
            console.print(formatted_content, mode="raw")
