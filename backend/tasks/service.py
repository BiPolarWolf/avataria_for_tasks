from .repository import TaskRepository
from sqlmodel import Session
from .models import Task
from users.models import User



class TaskService:
    def __init__(self,db:Session):
        self.repo = TaskRepository(db)

    

    def get_task(self,task_id:int) -> Task:
        task = self.repo.get_task_by_id(task_id)

        if task is None: 
            raise ValueError('Задача не найдена')
        
        return task
    

    def task_delete(self,task_id:int):
        task = self.repo.get_task_by_id(task_id)
        if task is None : 
            raise ValueError('Задача не найдена')
        
        return self.repo.delete_task(task)
    

    def get_tasks(self, author : User):
        tasks = self.repo.get_tasks_all(author)
        return tasks
    
