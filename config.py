from configparser import ConfigParser
from datetime import timedelta, timezone

cfg = ConfigParser()
cfg.read("config.ini")

TZ_OFFSET = cfg.getint("time", "timezone_offset")
TZ = timezone(timedelta(hours=TZ_OFFSET))
