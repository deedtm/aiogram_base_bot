from os import sep

from config import cfg

DB = cfg.get("database", "path")
DB_PATH = sep.join(DB.split(".")) + ".db"

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
