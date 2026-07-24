from typing import List

from sqlalchemy.orm import selectinload
from sqlmodel import Session, desc, or_, select

from tags.models import Tag
from users.models import User

from .models import Note


class NoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_note_by_id(self, note_id: int) -> Note | None:
        query = select(Note).options(selectinload(Note.tags)).where(Note.id == note_id)
        return self.db.exec(query).first()

    def get_notes_all(
        self,
        current_user: User,
        search: str | None = None,
        tag_ids: list[int] | None = None,
    ) -> List[Note]:
        query = (
            select(Note)
            .options(selectinload(Note.tags))
            .where(Note.author_id == current_user.id)
            .order_by(desc(Note.date_update))
        )

        # Поиск по заголовку и тексту — на стороне БД.
        if search:
            pattern = f"%{search}%"
            query = query.where(or_(Note.title.ilike(pattern), Note.text.ilike(pattern)))

        # Фильтр по тегам: запись должна иметь хотя бы один из выбранных тегов.
        if tag_ids:
            query = query.where(Note.tags.any(Tag.id.in_(tag_ids)))

        return self.db.exec(query).all()

    def get_user_tags_by_ids(self, current_user: User, tag_ids: list[int]) -> List[Tag]:
        if not tag_ids:
            return []

        query = select(Tag).where(Tag.author_id == current_user.id, Tag.id.in_(tag_ids))
        return self.db.exec(query).all()

    def __create_or_update_note(self, note: Note) -> Note:
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def create_note(self, note: Note) -> Note:
        return self.__create_or_update_note(note)

    def update_note(self, note: Note) -> Note:
        return self.__create_or_update_note(note)

    def delete_note(self, note: Note) -> Note:
        note.tags.clear()
        self.db.add(note)
        self.db.commit()
        self.db.delete(note)
        self.db.commit()
        return note
