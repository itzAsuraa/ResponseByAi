import re
from os import environ, getenv


API_ID = environ.get("API_ID", "")
API_HASH = environ.get("API_HASH", "")
BOT_TOKEN = environ.get("BOT_TOKEN", "")
OWNER_ID = int(environ.get("OWNER_ID", ""))
MONGO_URL = environ.get("MONGO_URL", "")
LOG_GROUP = environ.get("LOG_GROUP", "-1002100219353")
AUTH_CHANNEL = int(environ.get("AUTH_CHANNEL", ""))
FSUB = environ.get("FSUB", True)