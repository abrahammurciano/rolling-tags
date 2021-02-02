import discord
import config
from modules.error.error_logger import ErrorLogger
import discord.ext.commands.errors as discord_err


class ErrorHandler:
	"""
	Class that handles raised exceptions
	"""

	def __init__(self, error_logger: ErrorLogger) -> None:
		self.logger = error_logger

	def handle(self, error: Exception, message: discord.Message = None):
		if isinstance(error, discord_err.CommandInvokeError):
			self.handle(error.original, message)
		elif isinstance(error, discord.errors.Forbidden):
			self.logger.log_to_file(error, message)
		else:
			self.logger.log_to_file(error, message)
			self.logger.log_to_console(error, message)
