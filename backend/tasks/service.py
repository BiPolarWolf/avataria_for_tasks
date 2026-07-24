from enum import Enum
from .repository import TaskRepository
from sqlmodel import Session
from .models import Task, TaskCreate, TaskUpdate
from users.models import User
from typing import Optional
from exceptions import TaskCompletedAlreadyError, TaskIncorrectAuthorError,TaskNotFoundError, TagNotFoundError
from datetime import datetime, timezone

class TaskStatus(str, Enum):
    active = "active"
    completed = "completed"

class TaskService:
    def __init__(self,db:Session):
        self.repo = TaskRepository(db)

    def get_tasks(
        self,
        current_user : User,
        status: Optional[TaskStatus] = None,
        search: Optional[str] = None,
        tag_ids: Optional[list[int]] = None,
    ):

        if status == TaskStatus.active:
            tasks = self.repo.get_tasks_active(current_user, search, tag_ids)

        elif status == TaskStatus.completed:
            tasks = self.repo.get_tasks_completed(current_user, search, tag_ids)

        else:
            tasks = self.repo.get_tasks_all(current_user, search, tag_ids)
        return tasks


    def get_task(self,task_id:int,current_user:User) -> Task:
        task = self.repo.get_task_by_id(task_id)

        if task is None:
            raise TaskNotFoundError('Задачи с таким id не существует')

        if task.author_id != current_user.id:
            raise TaskIncorrectAuthorError('Это не ваша задача')

        return task


    def get_user_tasks_stats(self,current_user:User) -> Task:

        stats = self.repo.get_user_tasks_stats(current_user)

        return stats


    def __get_user_tags(self, tag_ids: list[int], current_user: User):
        unique_tag_ids = list(dict.fromkeys(tag_ids))
        tags = self.repo.get_user_tags_by_ids(current_user, unique_tag_ids)

        if len(tags) != len(unique_tag_ids):
            raise TagNotFoundError("Один или несколько тегов не найдены или не принадлежат вам")

        return tags


    def complete_task(self,task_id:int,current_user:User) -> Task:

        task = self.repo.get_task_by_id(task_id)

        if task is None:
            raise TaskNotFoundError('Задачи с таким id не существует')

        if task.author_id != current_user.id:
            raise TaskIncorrectAuthorError('Это не ваша задача')

        if task.status is True:
            raise TaskCompletedAlreadyError('Задача уже выполнена')
        else:
            task.status = True
            task.completed_at = datetime.now(timezone.utc)
            return self.repo.update_task(task)


    def update_task(self,task_data:TaskUpdate,current_user:User) -> Task:
        task = self.repo.get_task_by_id(task_data.id)

        if task is None:
            raise TaskNotFoundError('Задачи с таким id не существует')

        elif task.author_id != current_user.id:
            raise TaskIncorrectAuthorError('Это не ваша задача')

        elif task.status is True:
            raise TaskCompletedAlreadyError('Нельзя редактировать завершенную задачу')
        else:
            task_update = task_data.model_dump(exclude_unset=True, exclude={"id", "status"})

            if "tag_ids" in task_update:
                task.tags = self.__get_user_tags(task_update.pop("tag_ids"), current_user)

            for field, value in task_update.items():
                setattr(task, field, value)

            return self.repo.update_task(task)




    def create_task(self,task_data:TaskCreate,current_user:User) -> Task:
        task_dict = task_data.model_dump(exclude={"tag_ids"})

        task_dict.update({'author_id':current_user.id})

        db_task = Task.model_validate(task_dict)
        db_task.tags = self.__get_user_tags(task_data.tag_ids, current_user)

        return self.repo.create_task(db_task)




    def task_delete(self,task_id:int,current_user:User) -> Task:
        task = self.repo.get_task_by_id(task_id)
        if task is None :
            raise TaskNotFoundError('Задачи с таким id не существует')

        if task.author_id != current_user.id:
            raise TaskIncorrectAuthorError('Это не ваша задача')

        return self.repo.delete_task(task)
