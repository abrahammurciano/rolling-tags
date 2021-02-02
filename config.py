from dotenv.main import load_dotenv
import os

load_dotenv()

# Discord setup
token = os.getenv("DISCORD_TOKEN")

prefix = "rt."
