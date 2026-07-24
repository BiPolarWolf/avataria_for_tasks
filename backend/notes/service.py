from datetime import datetime, timezone

from sqlmodel import Session

from exceptions import NoteIncorrectAuthorError, NoteNotFoundError, TagNotFoundError
from users.models import User

from .models import Note, NoteCreate, NoteUpdate
from .repository import NoteRepository


class NoteService:
    def __init__(self, db: Session):
        self.repo = NoteRepository(db)

    def get_notes(
        self,
        current_user: User,
        search: str | None = None,
        tag_ids: list[int] | None = None,
    ):
        return self.repo.get_notes_all(current_user, search, tag_ids)

    def get_note(self, note_id: int, current_user: User) -> Note:
        note = self.repo.get_note_by_id(note_id)

        if note is None:
            raise NoteNotFoundError("Записки с таким id не существует")

        if note.author_id != current_user.id:
            raise NoteIncorrectAuthorError("Это не ваша записка")

        return note

    def __get_user_tags(self, tag_ids: list[int], current_user: User):
        unique_tag_ids = list(dict.fromkeys(tag_ids))
        tags = self.repo.get_user_tags_by_ids(current_user, unique_tag_ids)

        if len(tags) != len(unique_tag_ids):
            raise TagNotFoundError("Один или несколько тегов не найдены или не принадлежат вам")

        return tags

    def create_note(self, note_data: NoteCreate, current_user: User) -> Note:
        note_dict = note_data.model_dump(exclude={"tag_ids"})
        note_dict.update({"author_id": current_user.id})

        db_note = Note.model_validate(note_dict)
        db_note.tags = self.__get_user_tags(note_data.tag_ids, current_user)

        return self.repo.create_note(db_note)

    def update_note(self, note_data: NoteUpdate, current_user: User) -> Note:
        note = self.get_note(note_data.id, current_user)
        note_update = note_data.model_dump(exclude_unset=True)

        if "tag_ids" in note_update:
            note.tags = self.__get_user_tags(note_update.pop("tag_ids"), current_user)

        for field, value in note_update.items():
            setattr(note, field, value)

        note.date_update = datetime.now(timezone.utc)

        return self.repo.update_note(note)

    def delete_note(self, note_id: int, current_user: User) -> Note:
        note = self.get_note(note_id, current_user)
        return self.repo.delete_note(note)

    def get_similar_notes(self, note_id: int, current_user: User):
        self.get_note(note_id, current_user)

        return {
            "detail": "Поиск похожих записок пока не доработан. Роут уже готов для будущей логики embedding + SentenceTransformers.",
            "items": [],
        }
