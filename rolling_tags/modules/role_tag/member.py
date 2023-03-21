from .role import Role
import discord
import logging

logger = logging.getLogger(f"rolling_tags.{__name__}")


class Member:
    """
    Represents a member and their role tags
    """

    __slots__ = ("inner_member", "name_sep", "tag_sep", "base_name")

    def __init__(self, member: discord.Member, name_sep: str, tag_sep: str = " "):
        self.inner_member = member
        self.name_sep = name_sep
        self.tag_sep = tag_sep
        self.base_name = (
            member.nick.rsplit(name_sep, 1)[0].strip()
            if member.nick is not None
            else member.display_name
        )

    def current_tags(self) -> tuple[str, ...]:
        """Gets a tuple of tags the user currently has in their nickname"""
        if self.inner_member.nick is None:
            return ()
        split: list[str] = self.inner_member.nick.split(
            self.base_name + self.name_sep, 1
        )
        if len(split) > 1:
            return tuple(split[1].split(self.tag_sep))
        return ()

    def tags(self) -> tuple[str, ...]:
        """Gets a tuple of tags the user should have based on their roles"""
        roles = (
            Role(r, self.name_sep)
            for r in sorted(
                self.inner_member.roles, key=lambda role: role.position, reverse=True
            )
        )
        return tuple(role.tag.strip() for role in roles if role.has_tag())

    def tags_str(self) -> str:
        """Gets a string to append to a member's name to represent their tags"""
        tags = self.tags()
        return (self.name_sep + self.tag_sep.join(tags)) if tags else ""

    async def apply_tags(self):
        """Applies all the tags of the member's roles to their nickname."""
        new_nick = self.base_name + self.tags_str()
        old_nick = self.inner_member.display_name
        if old_nick == new_nick[:32]:
            logger.debug(
                f"Skipping rename of {old_nick} to {new_nick} because they are the same up to 32 characters."
            )
            return
        try:
            await self.inner_member.edit(nick=new_nick[:32])
            logger.debug(f"Renamed {old_nick} to {new_nick}.")
        except discord.errors.Forbidden:
            logger.warning(
                f"Unable to rename {self.inner_member.display_name} to {new_nick} due"
                " to missing permissions."
            )
