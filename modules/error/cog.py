import sys
import utils.utils as utils
from discord.ext import commands
from modules.error.error_handler import ErrorHandler
from modules.error.error_logger import ErrorLogger


class ErrorLogCog(commands.Cog, name="Error Logs"):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.logger = ErrorLogger("err.log")
		self.handler = ErrorHandler(self.logger)

	@commands.Cog.listener()
	async def on_command_error(self, ctx: commands.Context, error: Exception):
		"""When a command exception is raised, log it in err.log and bot log channel"""
		await self.handler.handle(error, ctx.message)

	@commands.Cog.listener()
	async def on_error(self, event, *args, **kwargs):
		"""When an exception is raised, log it in err.log and bot log channel"""

		_, error, _ = sys.exc_info()
		self.handler.handle(error)


# setup functions for bot
def setup(bot: commands.Bot):
	cog = ErrorLogCog(bot)
	bot.add_cog(cog)
	bot.on_error = cog.on_error