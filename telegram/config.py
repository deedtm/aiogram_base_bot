import os

from aiogram.client.default import DefaultBotProperties

from config import cfg

######### [config.ini]
PARSE_MODE = cfg.get("telegram", "parse_mode")
DISABLE_LINK_PREVIEW = cfg.getboolean("telegram", "disable_link_preview")
DROP_PENDING_UPDATES = cfg.getboolean("telegram", "drop_pending_updates")

DEFAULT_BOT_PROPERTIES = DefaultBotProperties(
    parse_mode=PARSE_MODE, link_preview_is_disabled=DISABLE_LINK_PREVIEW
)

BACK_PREFIX = cfg.get("telegram", "back_prefix")
USERS_LIST_AMOUNT = cfg.getint("telegram", "users_list_amount")

TOKEN = os.getenv("BOT_TOKEN")
######### [config.ini]

USERNAME_LINK_FORMAT = "https://t.me/{username}"
USER_ID_LINK_FORMAT = "tg://user?id={id}"
CHANNEL_ID_LINK_FORMAT = "https://t.me/c/{id}"

CHANNEL_POST_LINK_FORMAT = USERNAME_LINK_FORMAT + "/{post_id}"
CHANNEL_ID_POST_LINK_FORMAT = CHANNEL_ID_LINK_FORMAT + "/{post_id}"
