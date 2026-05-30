from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlalchemy import Column, JSON
from sqlmodel import Field, Relationship, SQLModel

from tags.models import NoteTagLink, TagRead
from users.models import User


if TYPE_CHECKING:
    from tags.models import Tag


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    title: str = Field(max_length=100)

    author_id: int = Field(foreign_key="user.id", index=True)
    author: "User" = Relationship(back_populates="notes")

    text: str = Field(max_length=1000)

    date_create: datetime = Field(default_factory=utc_now)
    
    # default_factory: авто-заполнение при INSERT (создании объекта)
    # onupdate: инструкция для SQLAlchemy перезаписывать время при UPDATE (изменении строки в БД)
    date_update: datetime = Field(default_factory=utc_now, sa_column_kwargs={"onupdate": utc_now})

    tags: List["Tag"] = Relationship(back_populates="notes", link_model=NoteTagLink)

    importans: int = Field(default=1, ge=1, le=10)
    theme: str = Field(default="neutral_paper", max_length=100)

    # Временно храним vector embedding как JSON-массив чисел.
    # Позже это поле можно заменить на pgvector.Vector через миграцию Postgres.
    embedding: list[float] | None = Field(default=None, sa_column=Column(JSON, nullable=True))


class NoteCreate(SQLModel):
    title: str = Field(max_length=100)
    text: str = Field(max_length=1000)
    tag_ids: list[int] = Field(default_factory=list)
    importans: int = Field(default=1, ge=1, le=10)
    theme: str = Field(default="neutral_paper", max_length=100)
    embedding: list[float] | None = None


class NoteUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=100)
    text: str | None = Field(default=None, max_length=1000)
    tag_ids: list[int] | None = None
    importans: int | None = Field(default=None, ge=1, le=10)
    theme: str | None = Field(default=None, max_length=100)
    embedding: list[float] | None = None


class NoteRead(SQLModel):
    id: int
    title: str
    author_id: int
    text: str
    date_create: datetime
    date_update: datetime
    importans: int
    theme: str
    embedding: list[float] | None = None
    tags: list[TagRead] = []
