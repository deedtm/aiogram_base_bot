from .config import HYPERLINK_FORMAT as HL_FMT


def hyperlink(link: str, text: str):
    return HL_FMT.format(link=link, text=text)
