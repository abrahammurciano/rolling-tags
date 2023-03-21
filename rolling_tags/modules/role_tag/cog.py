from .role import Role
from .member import Member
from discord.ext import commands
import discord
import logging

logger = logging.getLogger(f"rolling_tags.{__name__}")


class RoleTagsCog(commands.Cog, name="Role Tags"):  # type: ignore[call-arg]
    __slots__ = ("bot", "separator")

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.separator = " | "

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.display_name == after.display_name and before.roles == after.roles:
            return

        logger.debug(
            f'Member {after.display_name} changed in guild "{before.guild.name}"'
        )
        member = Member(after, self.separator)
        if member.current_tags() != member.tags():
            await member.apply_tags()

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        before_role = Role(before, self.separator)
        after_role = Role(after, self.separator)
        if before_role.tag != after_role.tag:
            logger.debug(
                f'Role "{before.name}" was renamed to "{after.name}" in guild'
                f' "{after.guild.name}".'
            )
            for member in after.members:
                await Member(member, self.separator).apply_tags()


def setup(bot: commands.Bot):
    bot.add_cog(RoleTagsCog(bot))
