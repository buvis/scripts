from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime
    from pathlib import Path

from .zettel_fixer import ZettelFixer
from .zettel_formatter import ZettelFormatter
from .zettel_parser import ZettelParser
from .zettel_raw_data import ZettelRawData


class Zettel:
    def __init__(self: Zettel) -> None:
        self._raw_data = ZettelRawData()

    def replace_raw_data(self: Zettel, raw_data: ZettelRawData) -> None:
        self._raw_data = raw_data

    @staticmethod
    def create_from_file(file_path: Path) -> Zettel:
        zettel = Zettel()
        zettel.replace_raw_data(ZettelParser.from_file(file_path))
        zettel.ensure_consistency()
        zettel.alias_attributes()
        return zettel

    def ensure_consistency(self: Zettel) -> None:
        ZettelFixer.ensure_consistency(self._raw_data)

    def alias_attributes(self: Zettel) -> None:
        for key, value in {
            **self._raw_data.metadata,
            **self._raw_data.reference,
        }.items():
            setattr(self, key, value)

    @property
    def id(self: Zettel) -> int | None:
        if self._raw_data.metadata.get("id", None) is None:
            return None
        try:
            return int(self._raw_data.metadata["id"])
        except ValueError:
            return None

    @id.setter
    def id(self: Zettel, value: int) -> None:
        try:
            self._raw_data.metadata["id"] = int(value)
        except ValueError as err:
            raise ValueError from err
        self.ensure_consistency()

    @property
    def title(self: Zettel) -> str | None:
        if self._raw_data.metadata.get("title", None) is None:
            return None

        return str(self._raw_data.metadata["title"])

    @title.setter
    def title(self: Zettel, value: str) -> None:
        self._raw_data.metadata["title"] = str(value)
        self.ensure_consistency()

    @property
    def date(self: Zettel) -> datetime | None:
        if self._raw_data.metadata.get("date", None) is None:
            return None

        return self._raw_data.metadata["date"]

    @date.setter
    def date(self: Zettel, value: datetime) -> None:
        self._raw_data.metadata["date"] = value
        self.ensure_consistency()

    @property
    def type(self: Zettel) -> str | None:
        if self._raw_data.metadata.get("type", None) is None:
            return None

        return str(self._raw_data.metadata["type"])

    @type.setter
    def type(self: Zettel, value: str) -> None:
        self._raw_data.metadata["type"] = str(value)
        self.ensure_consistency()

    @property
    def tags(self: Zettel) -> list | None:
        if self._raw_data.metadata.get("tags", None) is None:
            return None
        return self._raw_data.metadata["tags"]

    @tags.setter
    def tags(self: Zettel, value: list[str]) -> None:
        if not isinstance(value, list):
            value = [value]

        self._raw_data.metadata["tags"] = value
        self.ensure_consistency()

    @property
    def publish(self: Zettel) -> bool:
        if self._raw_data.metadata.get("publish", None) is None:
            return False
        return self._raw_data.metadata["publish"]

    @publish.setter
    def publish(self: Zettel, value: bool) -> None:
        if value:
            self._raw_data.metadata["publish"] = True
        else:
            self._raw_data.metadata["publish"] = False
        self.ensure_consistency()

    @property
    def processed(self: Zettel) -> bool:
        if self._raw_data.metadata.get("processed", None) is None:
            return False
        return self._raw_data.metadata["processed"]

    @processed.setter
    def processed(self: Zettel, value: bool) -> None:
        if value:
            self._raw_data.metadata["processed"] = True
        else:
            self._raw_data.metadata["processed"] = False
        self.ensure_consistency()

    def to_formatted_markdown(self: Zettel) -> str:
        return ZettelFormatter.as_markdown(self._raw_data)
