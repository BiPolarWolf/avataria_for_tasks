
from sqlmodel import SQLModel, Field, UniqueConstraint , Relationship
from typing import List , TYPE_CHECKING


if TYPE_CHECKING:
    from tasks.models import Task

# Общие поля
class UserBase(SQLModel):
    username: str = Field(index=True)
    email: str = Field(index=True) 


# Схема для POST запроса (теперь с полем password)
class UserCreate(UserBase):
    password: str  # Клиент отправляет "password"


class LoginRequest(SQLModel):
    login: str
    password: str


# Модель для базы данных (с полем hashed_password)
class User(UserBase, table=True):

    __table_args__ = (UniqueConstraint('username','email',name='unique_user_identity'),)

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    is_verified : bool = Field(default=False)

    tasks : List['Task'] = Relationship(back_populates='author')


class Profile(SQLModel):
    id : int
    username : str
    email: str
    is_verified : bool



class Token(SQLModel):
    access_token : str
    token_type : str
