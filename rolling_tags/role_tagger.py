import logging
from typing import overload

from discord import Forbidden, Role

from .guild_settings import GuildSettings

logger = logging.getLogger(__name__)


class RoleTagger:
    __slots__ = ("role", "base_name", "tag")

    def __init__(self, role: Role) -> None:
        """Manages the tag of a role.

        Args:
            role: The role whose tags to manage.
        """

        self.role = role
        split = self.role.name.rsplit("|", 1)
        self.tag: str | None = (
            split[1].strip().replace(" ", "-") if len(split) == 2 else None
        )
