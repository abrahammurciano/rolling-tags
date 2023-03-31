from dotenv.main import load_dotenv
import os
from logging import Logger, DEBUG, ERROR, StreamHandler
from discord_lumberjack.handlers import DiscordChannelHandler
from discord_lumberjack.message_creators import EmbedMessageCreator

load_dotenv()

# Discord setup
token = os.environ["DISCORD_TOKEN"]
debug_channel = (
    int(os.environ["DEBUG_CHANNEL"]) if "DEBUG_CHANNEL" in os.environ else None
)
error_channel = (
    int(os.environ["ERROR_CHANNEL"]) if "ERROR_CHANNEL" in os.environ else None
)


def setup_logger(logger: Logger):
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
