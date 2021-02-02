from datetime import datetime
from discord.channel import TextChannel
from discord.ext import commands
import traceback
import discord


class ErrorLogger:
	def __init__(self, log_file: str) -> None:
		self.log_file = log_file

	def log_to_file(self, error: Exception, message: discord.Message = None):
		"""appends the date and logs text to a file"""
		with open(self.log_file, "a", encoding="utf-8") as f:
			# write the current time and log text at end of file
			f.write(str(datetime.now()) + "\n")
			f.write(self.__get_err_text(error, message) + "\n")
			f.write("--------------------------\n")

	def log_to_console(self, error: Exception, message: discord.Message = None):
		print(self.__get_err_text(error, message))

	def __get_err_text(self, error: Exception, message: discord.Message = None):
		trace = traceback.format_exc()
		description = trace if trace != "NoneType: None\n" else str(error)
		if message is None:
			return description
		return self.__attach_context(description, message)

	def __attach_context(self, description: str, message: discord.Message):
		"""returns human readable command error for logging in log channel"""
		return (
			f"Author:\n{message.author} ({message.author.display_name})\n\n"
			f"Channel:\n{message.channel}\n\n"
			f"Message:\n{message.content}\n\n"
			f"Error:\n{description}\n"
		)