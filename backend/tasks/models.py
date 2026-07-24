
from sqlmodel import SQLModel, Field , Relationship
from datetime import datetime, timezone
from users.models import User
from typing import TYPE_CHECKING, List

from tags.models import TaskTagLink, TagRead


if TYPE_CHECKING:
    from users.models import User
    from tags.models import Tag

class Task(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Необязательный заголовок задачи (как у записей).
    title: str | None = Field(default=None, max_length=100)

    description : str
    complexity : int = Field(default=1,le=5)
    author_id : int = Field(foreign_key='user.id')
    author : "User" = Relationship(back_populates='tasks')
    status : bool = Field(default=False)

    tags: List["Tag"] = Relationship(back_populates="tasks", link_model=TaskTagLink)


    # Добавляем новое поле
    # Если в итоге оно должно быть обязательным, пока всё равно ставим default (или None),
    # чтобы SQLModel не ругался до применения миграции.
    completed_at: datetime | None = Field(default=None)


class TaskCreate(SQLModel):
    title: str | None = Field(default=None, max_length=100)
    description : str
    complexity : int = Field(default=1,le=5)
    tag_ids: list[int] = Field(default_factory=list)


class TaskUpdate(SQLModel):
    id: int
    title: str | None = Field(default=None, max_length=100)
    description : str
    complexity : int = Field(default=1,le=5)
    status : bool = Field(default=False)
    tag_ids: list[int] | None = None


class TaskRead(SQLModel):
    id: int
    created_at: datetime
    title: str | None = None
    description: str
    complexity: int
    author_id: int
    status: bool
    completed_at: datetime | None = None
    tags: list[TagRead] = []
