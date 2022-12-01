from .role import Role
from .member import Member
from discord.ext import commands
import discord
import logging

logger = logging.getLogger(f"rolling_tags.{__name__}")


class RoleTagsCog(commands.Cog, name="Role Tags"):  # type: ignore[call-arg]
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.display_name == after.display_name and tuple(
            r.id for r in before.roles
        ) == tuple(r.id for r in after.roles):
            return

        logger.debug(
            f'Member {after.display_name} changed in guild "{before.guild.name}"'
        )
        member = Member(after)
        if member.current_tags() != member.tags():
            await member.apply_tags()

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        before_role = Role(before)
        after_role = Role(after)
        if before_role.tag != after_role.tag:
            logger.debug(
                f'Role "{before.name}" was renamed to "{after.name}" in guild'
                f' "{after.guild.name}".'
            )
            for member in after.members:
                await Member(member).apply_tags()


def setup(bot: commands.Bot):
    bot.add_cog(RoleTagsCog(bot))
