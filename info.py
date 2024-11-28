from dotenv import load_dotenv

load_dotenv()

from os import getenv

API_ID = getenv("API_ID", "")
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = int(getenv("OWNER_ID", 7453278496))
MONGO_URL = getenv("MONGO_URL", "")
AUTH_CHANNEL = int(getenv("AUTH_CHANNEL", ""))
FSUB = getenv("FSUB", True)