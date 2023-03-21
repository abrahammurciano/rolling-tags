from pathlib import Path
import discord
import rolling_tags.config as config
from discord.ext import commands
import logging

from rolling_tags.setup_logger import setup_logger

logger = logging.getLogger("rolling_tags")


def main():
    setup_logger(logger)
    # allows privledged intents for monitoring members joining, roles editing, and role assignments (has to be enabled for the bot in Discord dev)
    intents = discord.Intents.default()
    intents.members = True

    client = commands.Bot(config.prefix, intents=intents)  # bot command prefix

    # Get the modules of all cogs whose directory structure is modules/<module_name>/cog.py
    for folder in (Path(__file__).parent / "modules").iterdir():
        if (folder / "cog.py").is_file():
            client.load_extension(f"{__package__}.modules.{folder.name}.cog")

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
        logger.exception("An unexpected error has occurred.")

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
