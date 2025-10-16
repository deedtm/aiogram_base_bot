from pydantic import BaseModel


class Middlewares(BaseModel):
    wait_message: str


__all__ = ("Middlewares",)
