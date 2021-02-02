from discord.ext import commands
import discord
from discord.ext.commands.core import is_nsfw


class NewHelpCommand(commands.MinimalHelpCommand):
	"""Custom help command override using embeds"""

	# embed colour
	COLOUR = discord.Colour.from_rgb(249, 142, 142)

	def get_ending_note(self):
		"""Returns note to display at the bottom"""
		prefix = self.clean_prefix
		invoked_with = self.invoked_with
		return f"Use {prefix}{invoked_with} to show this message."

	async def send_bot_help(self, mapping: dict):
		"""implements bot command help page"""
		embed = discord.Embed(
			title="Add tags to members based on their roles!", colour=self.COLOUR
		)

		embed.add_field(
			name="Setting tags to roles",
			value=(
				'To add a tag to a role, rename the role to "Role Name | *tag*", and'
				" everyone with that role will have that *tag* appended to their"
				" name.\n\nYou can use emojis, symbols, words, or anything you like in"
				' place of *tag*.\n\nFor example if you rename the role "Superuser" to'
				' "Superuser | #", then our buddy Linus, who is a member of that role,'
				' will have their name changed to "Linus | #" within the server.'
			),
			inline=False,
		)

		embed.add_field(
			name="Multiple tags",
			value=(
				"Users belonging to multiple roles which have tags will have all the"
				" relevant tags appended to their name. (Note, there is a 32 character"
				" limit on names, so avoid long tags.)"
			),
			inline=False,
		)

		embed.add_field(
			name="Changing Roles/Nicknames",
			value=(
				"Whenever a member's nickname is changed or their roles are changed,"
				" the bot automatically reapplies tags."
			),
			inline=False,
		)
		
		embed.add_field(
			name="Note:",
			value=(
				"There is currently no way for the bot to change the nickname of the"
				" server owner, so they are the only person who will remain unaffected"
				" by the bot."
			),
			inline=False,
		)

		embed.set_footer(text=self.get_ending_note())
		await self.get_destination().send(embed=embed)
