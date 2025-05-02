from . import _config

PARSE_MODE = _config.get("telegram", "parse_mode")
DISABLE_LINK_PREVIEW = _config.getboolean("telegram", "disable_link_preview")
DROP_PENDING_UPDATES = _config.getboolean("telegram", "drop_pending_updates")
BACK_PREFIX = _config.get("telegram", "back_prefix")
USERS_LIST_AMOUNT = _config.getint("telegram", "users_list_amount")

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
