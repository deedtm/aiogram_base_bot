import sqlite3
from config.database import DB_PATH

conn = sqlite3.connect(DB_PATH, autocommit=True)
cursor = conn.cursor()
