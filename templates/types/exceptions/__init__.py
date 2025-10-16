from pydantic import BaseModel


class Exceptions(BaseModel):
    base: str
    no_data: str
    retry: str
    no_args: str
    wrong_args: str
    user_not_found: str
    low_access: str
    low_access_to_set: str
    own_access: str
    over_access_set: str


__all__ = ("Exceptions",)
