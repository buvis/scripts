from buvis.domain.entity.zettel.zettel_raw_data import ZettelRawData

DEFAULT_TITLE = "Unknown title"


def set_default_title(zettel_raw_data: ZettelRawData) -> None:
    if (
        zettel_raw_data.metadata.get("title", None) is None
        and getattr(zettel_raw_data, "sections", None) is not None
    ):
        first_heading, _ = zettel_raw_data.sections[0]

        if first_heading.startswith("# "):
            zettel_raw_data.metadata["title"] = first_heading[2:]

    # Fallback to default title
    if zettel_raw_data.metadata.get("title", None) is None:
        zettel_raw_data.metadata["title"] = DEFAULT_TITLE
