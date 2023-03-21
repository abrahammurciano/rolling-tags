from logging import Logger, DEBUG, ERROR, StreamHandler
from discord_lumberjack.handlers import DiscordChannelHandler
from discord_lumberjack.message_creators import EmbedMessageCreator
from .config import token, debug_channel, error_channel


def setup_logger(logger: Logger):
    logger.setLevel(DEBUG)
    logger.addHandler(
        DiscordChannelHandler(token, debug_channel, DEBUG, EmbedMessageCreator())
    )
    logger.addHandler(
        DiscordChannelHandler(token, error_channel, ERROR, EmbedMessageCreator())
    )
    logger.addHandler(StreamHandler())
