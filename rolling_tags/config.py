from dotenv.main import load_dotenv
import os

load_dotenv()

# Discord setup
token = os.environ["DISCORD_TOKEN"]
debug_channel = int(os.environ["DEBUG_CHANNEL"])
error_channel = int(os.environ["ERROR_CHANNEL"])

prefix = "rt."
