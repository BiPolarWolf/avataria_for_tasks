from typing import List

from sqlmodel import Session, select

from users.models import User

from .models import Tag


class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_tag_by_id(self, tag_id: int) -> Tag | None:
        query = select(Tag).where(Tag.id == tag_id)
        return self.db.exec(query).first()

    def get_tags_all(self, current_user: User) -> List[Tag]:
        query = select(Tag).where(Tag.author_id == current_user.id)
        return self.db.exec(query).all()

    def __create_or_update_tag(self, tag: Tag) -> Tag:
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def create_tag(self, tag: Tag) -> Tag:
        return self.__create_or_update_tag(tag)

    def update_tag(self, tag: Tag) -> Tag:
        return self.__create_or_update_tag(tag)

    def untie_tag_from_notes(self, tag: Tag) -> Tag:
        tag.notes.clear()
        tag.tasks.clear()
        return self.__create_or_update_tag(tag)

    def delete_tag(self, tag: Tag) -> Tag:
        self.db.delete(tag)
        self.db.commit()
        return tag
