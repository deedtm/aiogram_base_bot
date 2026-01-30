from sqlalchemy import Column, Integer, Text

from .connect import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(Text, nullable=True)
    first_name = Column(Text, nullable=True)
    last_name = Column(Text, nullable=True)
    register_date = Column(Text, nullable=True)
    access_level = Column(Integer, default=1, nullable=False)
    favorite_color = Column(Text, nullable=True)
    favorite_food = Column(Text, nullable=True)
    favorite_work = Column(Text, nullable=True)
    favorite_pet = Column(Text, nullable=True)

    @property
    def as_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
