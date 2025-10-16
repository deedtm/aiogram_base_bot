from pydantic import BaseModel

class Keyboard(BaseModel):
    general: str
    id: str
    username: str
    first_name: str
    last_name: str
    phone_number: str
    location: str
    language_code: str
    url: str
