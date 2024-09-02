from buvis_scripts.core.domain.entity.zettel.zettel import Zettel

from .project_fixer import ProjectZettelFixer


class ProjectZettel(Zettel):
    def __init__(self: "ProjectZettel") -> None:
        super().__init__()

    def _ensure_consistency(self: "ProjectZettel") -> None:
        super()._ensure_consistency()
        ProjectZettelFixer.ensure_consistency(self._data)

    @property
    def log(self: "ProjectZettel") -> str:
        for section in self._data.sections:
            if section[0] == "## Log":
                return section[1]
        return ""
