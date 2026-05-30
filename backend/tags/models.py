from typing import TYPE_CHECKING, ClassVar, List

from sqlmodel import Field, Relationship, SQLModel

from users.models import User


if TYPE_CHECKING:
    from notes.models import Note


class NoteTagLink(SQLModel, table=True):
    note_id: int | None = Field(default=None, foreign_key="note.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)


class Tag(SQLModel, table=True):
    ICON_MAX_FILE_SIZE_BYTES: ClassVar[int] = 2 * 1024 * 1024
    ICON_MAX_WIDTH_PX: ClassVar[int] = 512
    ICON_MAX_HEIGHT_PX: ClassVar[int] = 512

    id: int | None = Field(default=None, primary_key=True)

    author_id: int = Field(foreign_key="user.id", index=True)
    author: "User" = Relationship(back_populates="tags")

    text: str = Field(max_length=100)
    color: str = Field(default="#EAD7BB", max_length=7, regex=r"^#[0-9A-Fa-f]{6}$")

    # Храним путь/URL иконки; проверку файла и пикселей лучше делать в upload-сервисе.
    icon: str | None = Field(default=None, max_length=255)

    notes: List["Note"] = Relationship(back_populates="tags", link_model=NoteTagLink)


class TagCreate(SQLModel):
    text: str = Field(max_length=100)
    color: str = Field(default="#EAD7BB", max_length=7, regex=r"^#[0-9A-Fa-f]{6}$")
    icon: str | None = Field(default=None, max_length=255)


class TagUpdate(SQLModel):
    text: str | None = Field(default=None, max_length=100)
    color: str | None = Field(default=None, max_length=7, regex=r"^#[0-9A-Fa-f]{6}$")
    icon: str | None = Field(default=None, max_length=255)


class TagRead(SQLModel):
    id: int
    author_id: int
    text: str
    color: str
    icon: str | None = None
