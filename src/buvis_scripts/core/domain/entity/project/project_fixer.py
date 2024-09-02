from buvis_scripts.core.domain.entity.zettel.zettel_data import ZettelData

from .fixers import (
    fix_lists_bullets,
    migrate_loop_log,
    normalize_sections_order,
)


class ProjectZettelFixer:
    @staticmethod
    def ensure_consistency(zettel_data: ZettelData) -> None:
        fix_lists_bullets(zettel_data)
        migrate_loop_log(zettel_data)
        normalize_sections_order(zettel_data)
