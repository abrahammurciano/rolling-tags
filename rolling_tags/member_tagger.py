import logging
from typing import cast, overload

from discord import Forbidden, Member
from parse import Result

from .guild_settings import GuildSettings
from .role_tagger import RoleTagger

logger = logging.getLogger(f"rolling_tags.{__name__}")


class MemberTagger:
    """Represents a member and their role tags."""

    __slots__ = ("base_name", "member", "new_settings", "old_settings")

    @overload
    def __init__(self, member: Member, settings: GuildSettings, /) -> None: ...

    @overload
    def __init__(
        self, member: Member, old_settings: GuildSettings, new_settings: GuildSettings
    ) -> None: ...

    @overload
    def __init__(
        self, member: Member, settings: GuildSettings, /, *, old_name: str, new_name: str
    ) -> None: ...

    def __init__(
        self,
        member: Member,
        old_settings: GuildSettings,
        new_settings: GuildSettings | None = None,
        *,
        old_name: str | None = None,
        new_name: str | None = None,
    ) -> None:
        """Manage the tags of a member.

        Args:
            member: The member whose tags to manage.
            settings: The guild's settings.
            old_settings: The guild's settings before the update.
            new_settings: The guild's settings after the update.
            old_name: The member's previous global display name, before a rename.
            new_name: The member's new global display name, after a rename.
        """
        self.member = member
        self.old_settings = old_settings
        self.new_settings = new_settings or old_settings
        self.base_name = self._parse_base_name(old_settings, old_name=old_name, new_name=new_name)

    def tags(self) -> tuple[str, ...]:
        """Get the tags the user should have based on their roles."""
        roles = (
            RoleTagger(r)
            for r in sorted(
                self.member.roles, key=lambda role: role.position, reverse=True
            )
        )
        return tuple(role.tag.strip() for role in roles if role.tag)

    async def update(self) -> None:
        """Apply all the tags of the member's roles to their nickname."""
        old_name = self.member.display_name
        new_name = self._format_name(self.new_settings)
        if old_name[:32] == new_name[:32]:
            logger.debug(
                f"Skipping rename of {old_name} to {new_name} because they are the same (up to 32 characters)."
            )
            return
        logger.info(f"Renaming {old_name} to {new_name}")
        try:
            await self.member.edit(nick=new_name[:32])
        except Forbidden:
            logger.warning(
                f"Could not rename {old_name} to {new_name} because I don't have permission."
            )

    def _format_name(self, settings: GuildSettings) -> str:
        """Drafts a new name for the member based on their roles.

        Args:
            settings: The guild's settings to use for formatting.
        """
        tags = self.tags()
        return (
            settings.format_string.format(
                t=settings.separator.join(tags), n=self.base_name
            )
            if tags
            else self.base_name
        )

    def _parse_base_name(
        self,
        settings: GuildSettings,
        *,
        old_name: str | None = None,
        new_name: str | None = None,
    ) -> str:
        """Extract the base name from the member's nickname.

        Args:
            settings: The guild's settings to use for parsing.
            old_name: The member's previous global display name, before a rename.
            new_name: The member's new global display name, after a rename.
        """
        result = settings.parser.parse(self.member.display_name)
        if result is None:
            parsed = self.member.display_name
        else:
            assert isinstance(result, Result)
            parsed = cast(dict[str, str], result.named).get("n", self.member.display_name)
        if old_name is not None and new_name is not None and parsed == old_name:
            return new_name
        return parsed
