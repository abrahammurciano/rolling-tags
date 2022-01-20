import os
import discord
import config
from discord.ext import commands
import logging
from discord_lumberjack.handlers import DiscordChannelHandler
from discord_lumberjack.message_creators import EmbedMessageCreator

# Set up logging
logger = logging.getLogger("rolling_tags")
logger.setLevel(logging.DEBUG)
logger.addHandler(
	DiscordChannelHandler(
		config.token, config.debug_channel, logging.DEBUG, EmbedMessageCreator()
	)
)
logger.addHandler(
	DiscordChannelHandler(
		config.token, config.error_channel, logging.ERROR, EmbedMessageCreator()
	)
)
logger.addHandler(logging.StreamHandler())
logging.getLogger().addHandler(logging.StreamHandler())


def main():
	# allows privledged intents for monitoring members joining, roles editing, and role assignments (has to be enabled for the bot in Discord dev)
	intents = discord.Intents.default()
	intents.members = True

	client = commands.Bot(config.prefix, intents=intents)  # bot command prefix

	# Get the modules of all cogs whose directory structure is modules/<module_name>/cog.py
	for folder in os.listdir("modules"):
		if os.path.exists(os.path.join("modules", folder, "cog.py")):
			client.load_extension(f"modules.{folder}.cog")

	@client.event
	async def on_ready():
		"""When discord is connected"""
		logger.info(f"{client.user.name} has connected to Discord!")
		await set_presence()

	@client.event
	async def on_guild_join(guild: discord.Guild):
		"""When the bot joins a guild"""
		logger.info(f"{client.user.name} has joined {guild.name}")
		await set_presence()

	@client.event
	async def on_error():
		"""When an error occurs"""
		logger.exception(f"An unexpected error has occurred.")

	async def set_presence():
		await client.change_presence(
			activity=discord.Activity(
				type=discord.ActivityType.listening,
				name=f"rt.help in {len(client.guilds)} servers. PUT MY ROLE ON TOP!",
			)
		)

	# Run Discord bot
	client.run(config.token)


if __name__ == "__main__":
	main()
