from . import _config
import os

DB = _config.get("database", "path")
DB_PATH = os.sep.join(DB.split(".")) + ".db"
