from pathlib import Path

from buvis.pybase.configuration import Configuration, ConfigurationKeyNotFoundError
from buvis.pybase.filesystem import DirTree

DEFAULT_TIDY_JUNK_EXTENSIONS = [
    ".cue",
    ".db",
    ".jpg",
    ".jpeg",
    ".lrc",
    ".m3u",
    ".m3u8",
    ".md",
    ".nfo",
    ".png",
    ".sfv",
    ".txt",
    ".url",
]


class CommandTidy:
    def __init__(self: "CommandTidy", cfg: Configuration) -> None:
        self.junk_extensions = cfg.get_configuration_item_or_default(
            "tidy_junk_extensions",
            DEFAULT_TIDY_JUNK_EXTENSIONS,
        )

        try:
            self.dir = Path(str(cfg.get_configuration_item("tidy_directory")))
        except ConfigurationKeyNotFoundError as e:
            raise ConfigurationKeyNotFoundError from e

    def execute(self: "CommandTidy") -> None:
        DirTree.merge_mac_metadata(self.dir)
        DirTree.normalize_file_extensions(self.dir)
        DirTree.delete_by_extension(self.dir, self.junk_extensions)
        DirTree.remove_empty_directories(self.dir)
