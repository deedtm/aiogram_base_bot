from pydantic import BaseModel

class Admin(BaseModel):
    general: str
    commands_list_fmt: str
    users: str
    users_list_fmt: str
    random_users: str
    getuser: str
    user_fmt: str
    access: str
