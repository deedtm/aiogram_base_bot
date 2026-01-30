from pydantic import BaseModel


class Quiz(BaseModel):
    start: str
    color: str
    food: str
    work: str
    pet: str
    end: str
