from sqlmodel import Session

from exceptions import TagAttachedToNotesError, TagIncorrectAuthorError, TagNotFoundError
from users.models import User

from .models import Tag, TagCreate, TagUpdate
from .repository import TagRepository


class TagService:
    def __init__(self, db: Session):
        self.repo = TagRepository(db)

    def get_tags(self, current_user: User):
        return self.repo.get_tags_all(current_user)

    def get_tag(self, tag_id: int, current_user: User) -> Tag:
        tag = self.repo.get_tag_by_id(tag_id)

        if tag is None:
            raise TagNotFoundError("Тега с таким id не существует")

        if tag.author_id != current_user.id:
            raise TagIncorrectAuthorError("Это не ваш тег")

        return tag

    def create_tag(self, tag_data: TagCreate, current_user: User) -> Tag:
        tag_dict = tag_data.model_dump()
        tag_dict.update({"author_id": current_user.id})
        db_tag = Tag.model_validate(tag_dict)
        return self.repo.create_tag(db_tag)

    def update_tag(self, tag_id: int, tag_data: TagUpdate, current_user: User) -> Tag:
        tag = self.get_tag(tag_id, current_user)

        for field, value in tag_data.model_dump(exclude_unset=True).items():
            setattr(tag, field, value)

        return self.repo.update_tag(tag)

    def untie_tag(self, tag_id: int, current_user: User) -> Tag:
        tag = self.get_tag(tag_id, current_user)
        return self.repo.untie_tag_from_notes(tag)

    def delete_tag(self, tag_id: int, current_user: User) -> Tag:
        tag = self.get_tag(tag_id, current_user)

        if tag.notes:
            raise TagAttachedToNotesError(
                "Нельзя удалить тег, пока он привязан к запискам. Сначала отвяжите тег."
            )

        return self.repo.delete_tag(tag)
