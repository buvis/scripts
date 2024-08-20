from buvis.domain.entity.zettel.zettel_raw_data import ZettelRawData


def align_h1_to_title(zettel_raw_data: ZettelRawData) -> None:
    title_heading = f"# {zettel_raw_data.metadata["title"]}"

    if len(zettel_raw_data.sections) > 0:
        first_heading, content = zettel_raw_data.sections[0]
    else:
        first_heading = ""
        content = ""

    if first_heading != title_heading:
        if first_heading != "" and not first_heading.startswith("# "):
            zettel_raw_data.sections.insert(0, (title_heading, ""))
        elif first_heading == "" or first_heading.startswith("# "):
            zettel_raw_data.sections[0] = (title_heading, content)
