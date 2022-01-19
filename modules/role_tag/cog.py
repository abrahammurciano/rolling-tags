from modules.role_tag.role import Role
from modules.role_tag.member import Member
from discord.ext import commands
import discord
import logging

logger = logging.getLogger(f"rolling_tags.{__name__}")


class RoleTagsCog(commands.Cog, name="Role Tags"):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_update(self, before: discord.Member, after: discord.Member):
		member = Member(after)
		if member.current_tags() == member.tags():
			return
		changed_str = (
			f'Name "{before.display_name}" changed to "{after.display_name}"'
			if before.display_name == after.display_name
			else (
				f"Roles ({', '.join(r.name for r in before.roles)}) changed to"
				f" ({', '.join(r.name for r in after.roles)})"
			)
		)

		logger.debug(
			f'Member "{after.display_name}" changed in guild "{after.guild.name}":'
			f" {changed_str}"
		)
		await member.apply_tags()

	@commands.Cog.listener()
	async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
		before_role = Role(before)
		after_role = Role(after)
		if before_role.tag != after_role.tag:
			logger.debug(f"Role {before.name} was renamed to {after.name}.")
			for member in after.members:
				await Member(member).apply_tags()


def setup(bot: commands.Bot):
	bot.add_cog(RoleTagsCog(bot))