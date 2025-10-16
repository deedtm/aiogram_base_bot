from os import path as p

from .config import JSONS_PATH


def get_json_content(name: str):
    with open(p.join(JSONS_PATH, name + ".json"), "r", encoding="utf-8") as f:
        return f.read()
