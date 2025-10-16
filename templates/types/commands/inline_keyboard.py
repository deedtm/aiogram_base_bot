from pydantic import BaseModel

class InlineKeyboard(BaseModel):
    general: str
    id: str
    username: str
    first_name: str
    last_name: str
    language_code: str
    url: str
    