from . import _config
import os

DB = _config.get("database", "path")
DB_PATH = os.sep.join(DB.split(".")) + ".db"
TABLE_NAME = _config.get("database", "table_name")
TABLE_COLUMNS = _config.get("database", "table_columns").split('\n')
