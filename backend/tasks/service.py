from .repository import TaskRepository
from sqlmodel import Session
from .models import Task, TaskCreate
from users.models import User
from exceptions import TaskCompletedAlreadyError, TaskIncorrectAuthorError,TaskNotFoundError



class TaskService:
    def __init__(self,db:Session):
        self.repo = TaskRepository(db)

    
    def get_tasks(self, current_user : User):
        tasks = self.repo.get_tasks_all(current_user)
        return tasks


    def get_task(self,task_id:int,current_user:User) -> Task:
        task = self.repo.get_task_by_id(task_id)

        if task is None: 
            raise TaskNotFoundError('Задачи с таким id не существует')
        
        if task.author_id != current_user.id:
            raise TaskIncorrectAuthorError('Это не ваша задача')
        
        return task
    

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
            return self.repo.update_task(task)

    

    def create_task(self,task_data:TaskCreate,current_user:User):
        task_dict = task_data.model_dump()

        task_dict.update({'author_id':current_user.id})

        db_task = Task.model_validate(task_dict)

        return self.repo.create_task(db_task)
    

    def task_delete(self,task_id:int):
        task = self.repo.get_task_by_id(task_id)
        if task is None : 
            raise ValueError('Задача не найдена')
        
        return self.repo.delete_task(task)
    

    
