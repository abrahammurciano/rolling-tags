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
		# For testing purposes only. Remove in a while
		if before.display_name != after.display_name and tuple(
			r.id for r in before.roles
		) != tuple(r.id for r in after.roles):
			logger.error(
				"Member nickname and roles changed at once! I thought this was"
				" impossible!"
			)

		if before.display_name != after.display_name:
			func = self.on_member_name_change
		elif tuple(r.id for r in before.roles) != tuple(r.id for r in after.roles):
			func = self.on_member_roles_change
		else:
			return
		await func(before, after)

	async def on_member_name_change(
		self, before: discord.Member, after: discord.Member
	):
		member = Member(after)
		if member.current_tags() != member.tags():
			logger.debug(
				f'Member nickname changed in guild "{before.guild.name}":'
				f' "{before.display_name}" -> "{after.display_name}"'
			)
			await member.apply_tags()

	async def on_member_roles_change(
		self, before: discord.Member, after: discord.Member
	):
		member = Member(after)
		if member.current_tags() != member.tags():
			logger.debug(
				f'Member "{after.display_name}" roles changed in guild'
				f' "{before.guild.name}": {[r.name for r in before.roles]} ->'
				f" {[r.name for r in after.roles]}"
			)
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