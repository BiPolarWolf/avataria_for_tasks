
from sqlmodel import SQLModel, Field , Relationship
from datetime import datetime, timezone
from users.models import User
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from users.models import User

class Task(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    description : str
    complexity : int = Field(default=1,max_length=5)
    author_id : int = Field(foreign_key='user.id')
    author : "User" = Relationship(back_populates='tasks')
