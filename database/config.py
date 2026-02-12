from os import getenv

USER = getenv("DB_USER")
PASSWORD = getenv("DB_PASSWORD")
HOST = getenv("DB_HOST")
PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
