from sqlmodel import Session, select ,desc ,func , or_
from sqlalchemy.orm import selectinload
from .models import Task
from tags.models import Tag
from users.models import User
from typing import Dict, List

class TaskRepository:


    def __init__(self,db : Session):
        self.db = db


    def get_task_by_id(self,task_id : int) -> Task | None:
        query = select(Task).options(selectinload(Task.tags)).where(Task.id == task_id)
        task = self.db.exec(query).first()
        return task if task else None


    def get_user_tags_by_ids(self, current_user: User, tag_ids: list[int]) -> List[Tag]:
        if not tag_ids:
            return []

        query = select(Tag).where(Tag.author_id == current_user.id, Tag.id.in_(tag_ids))
        return self.db.exec(query).all()


    def __apply_filters(self, query, search: str | None, tag_ids: list[int] | None):
        # Поиск по заголовку и описанию — на стороне БД.
        if search:
            pattern = f"%{search}%"
            query = query.where(or_(Task.title.ilike(pattern), Task.description.ilike(pattern)))

        # Фильтр по тегам: задача должна иметь хотя бы один из выбранных тегов.
        if tag_ids:
            query = query.where(Task.tags.any(Tag.id.in_(tag_ids)))

        return query


    def get_tasks_all(self, current_user:User, search: str | None = None, tag_ids: list[int] | None = None) -> List[Task]:
        query = select(Task).options(selectinload(Task.tags)).where(Task.author_id == current_user.id)
        query = self.__apply_filters(query, search, tag_ids)
        tasks = self.db.exec(query).all()
        return tasks


    def get_tasks_active(self, current_user:User, search: str | None = None, tag_ids: list[int] | None = None) -> List[Task]:
        query = (
            select(Task)
            .options(selectinload(Task.tags))
            .where(Task.author_id == current_user.id, Task.status == False)
            .order_by(desc(Task.created_at))
        )
        query = self.__apply_filters(query, search, tag_ids)
        tasks = self.db.exec(query).all()
        return tasks

    def get_tasks_completed(self, current_user:User, search: str | None = None, tag_ids: list[int] | None = None) -> List[Task]:
        query = (
            select(Task)
            .options(selectinload(Task.tags))
            .where(Task.author_id == current_user.id, Task.status == True)
            .order_by(desc(Task.completed_at))
        )
        query = self.__apply_filters(query, search, tag_ids)
        tasks = self.db.exec(query).all()
        return tasks


    def __create_or_update_task(self,task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return  task


    # Предположим, у тебя есть модель Task с полем status
    def get_user_tasks_stats(self, current_user:User) -> Dict[bool, int]:
        # Строим запрос: выбираем статус и считаем количество ID задач
        query = (
            select(Task.status, func.count(Task.id))
            .where(Task.author == current_user)
            .group_by(Task.status)
        )

        results = self.db.exec(query).all()

        # Превращаем результат [( 'completed', 5), ('in_progress', 2)] в красивый словарь
        return {status: count for status, count in results}

    def create_task(self,task:Task) -> Task:
        return self.__create_or_update_task(task)


    def update_task(self,task:Task) -> Task:
        return self.__create_or_update_task(task)


    def delete_task(self,task) -> Task:
        task.tags.clear()
        self.db.add(task)
        self.db.commit()
        self.db.delete(task)
        self.db.commit()
        return task
