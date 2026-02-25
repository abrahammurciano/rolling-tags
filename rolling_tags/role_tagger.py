import logging

from discord import Role

logger = logging.getLogger(__name__)


class RoleTagger:
    """Manages the tag of a role.

    Args:
        role: The role whose tags to manage.
    """

    __slots__ = ("role", "tag")

    def __init__(self, role: Role) -> None:
        self.role = role
        split = self.role.name.rsplit("|", 1)
        self.tag: str | None = (
            split[1].strip().replace(" ", "-") if len(split) == 2 else None
        )
