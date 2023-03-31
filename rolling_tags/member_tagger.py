import logging
from typing import overload

from discord import Forbidden, Member

from .guild_settings import GuildSettings
from .role_tagger import RoleTagger

logger = logging.getLogger(f"rolling_tags.{__name__}")


class MemberTagger:
    """
    Represents a member and their role tags
    """

    __slots__ = ("member", "base_name", "old_settings", "new_settings")

    @overload
    def __init__(self, member: Member, settings: GuildSettings, /) -> None:
        """Manages the tags of a member.

        Args:
            member: The member whose tags to manage.
            settings: The guild's settings.
        """

    @overload
    def __init__(
        self, member: Member, old_settings: GuildSettings, new_settings: GuildSettings
    ) -> None:
        """Manages the tag of a role.

        Args:
            member: The member whose tags to manage.
            old_settings: The guild's settings before the update.
            new_settings: The guild's settings after the update.
        """

    def __init__(
        self,
        member: Member,
        old_settings: GuildSettings,
        new_settings: GuildSettings | None = None,
    ):
        self.member = member
        self.old_settings = old_settings
        self.new_settings = new_settings or old_settings
        self.base_name = self._parse_base_name(old_settings)

    def tags(self) -> tuple[str, ...]:
        """A tuple of tags the user should have based on their roles"""
        roles = (
            RoleTagger(r)
            for r in sorted(
                self.member.roles, key=lambda role: role.position, reverse=True
            )
        )
        return tuple(role.tag.strip() for role in roles if role.tag)

    async def update(self) -> None:
        """Applies all the tags of the member's roles to their nickname.

        Args:
            custom_sep: A custom separator to use instead of the current one.
        """
        old_name = self.member.display_name
        new_name = self._format_name(self.new_settings)
        try:
            assert old_name[:32] != new_name[:32]
            logger.info(f"Renaming {old_name} to {new_name}")
            await self.member.edit(nick=new_name[:32])
        except Forbidden:
            logger.warning(
                f"Could not rename {old_name} to {new_name} because I don't have permission."
            )
        except AssertionError:
            logger.debug(
                f"Skipping rename of {old_name} to {new_name} because they are the same (up to 32 characters)."
            )

    def _format_name(self, settings: GuildSettings) -> str:
        """Drafts a new name for the member based on their roles.

        Args:
            settings: The guild's settings to use for formatting."""
        tags = self.tags()
        return (
            settings.format_string.format(
                t=settings.separator.join(tags), n=self.base_name
            )
            if tags
            else self.base_name
        )

    def _parse_base_name(self, settings: GuildSettings) -> str:
        """Extracts the base name from the member's nickname.

        Args:
            settings: The guild's settings to use for parsing."""
        result = settings.parser.parse(self.member.display_name)
        return (
            result.named.get("n", self.member.display_name)
            if result
            else self.member.display_name
        )
