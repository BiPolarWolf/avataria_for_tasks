
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, UniqueConstraint , Relationship
from typing import List , TYPE_CHECKING, Optional


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

    refresh_token: Optional["RefreshToken"] = Relationship(
        back_populates="user",
    )


class Profile(SQLModel):
    id : int
    username : str
    email: str
    is_verified : bool



class Token(SQLModel):
    access_token : str
    token_type : str


class RefreshToken(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Сам токен (лучше индексировать для быстрого поиска)
    token: str = Field(index=True, unique=True)
    
    # Когда токен протухнет
    expires_at: datetime
    
    # Дата создания (полезно для логов)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


    # Внешний ключ на юзера
    user_id: int = Field(foreign_key="user.id")
    
    # Обратная связь
    user: User = Relationship(back_populates="refresh_token")