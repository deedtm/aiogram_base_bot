from ..connect import get_session
from .user import User, UserCRUD

user_crud = UserCRUD(get_session)


__all__ = (
    "user_crud",
    "User",
)
