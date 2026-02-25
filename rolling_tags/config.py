import os
from logging import DEBUG, ERROR, Logger, StreamHandler

from discord_lumberjack.handlers import DiscordChannelHandler
from discord_lumberjack.message_creators import EmbedMessageCreator
from dotenv.main import load_dotenv

load_dotenv()

# Discord setup
token = os.environ["DISCORD_TOKEN"]
debug_channel = (
    int(os.environ["DEBUG_CHANNEL"]) if "DEBUG_CHANNEL" in os.environ else None
)
error_channel = (
    int(os.environ["ERROR_CHANNEL"]) if "ERROR_CHANNEL" in os.environ else None
)


def setup_logger(logger: Logger) -> None:
    logger.setLevel(DEBUG)
    if debug_channel:
        logger.addHandler(
            DiscordChannelHandler(token, debug_channel, DEBUG, EmbedMessageCreator())
        )
    if error_channel:
        logger.addHandler(
            DiscordChannelHandler(token, error_channel, ERROR, EmbedMessageCreator())
        )
    logger.addHandler(StreamHandler())
