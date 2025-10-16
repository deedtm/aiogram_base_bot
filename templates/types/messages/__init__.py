from pydantic import BaseModel


class Messages(BaseModel):
    text: str
    media: str


__all__ = ("Messages",)
