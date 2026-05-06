from sqlmodel import Session, select ,desc
from .models import Task
from users.models import User
from typing import List

class TaskRepository:


    def __init__(self,db : Session):
        self.db = db


    def get_task_by_id(self,task_id : int) -> Task | None:
        query = select(Task).where(Task.id == task_id)
        task = self.db.exec(query).first()
        return task if task else None
    

    def get_tasks_all(self, current_user:User) -> List[Task]:
        query = select(Task).where(Task.author_id == current_user.id)
        tasks = self.db.exec(query).all()
        return tasks
    

    def get_tasks_active(self, current_user:User) -> List[Task]:
        query = select(Task).where(Task.author_id == current_user.id,Task.status == False).order_by(desc(Task.created_at))
        tasks = self.db.exec(query).all()
        return tasks
    
    def get_tasks_completed(self, current_user:User) -> List[Task]:
        query = select(Task).where(Task.author_id == current_user.id,Task.status == True).order_by(desc(Task.created_at))
        tasks = self.db.exec(query).all()
        return tasks
    

    def __create_or_update_task(self,task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return  task



    def create_task(self,task:Task) -> Task:
        return self.__create_or_update_task(task)


    def update_task(self,task:Task) -> Task:
        return self.__create_or_update_task(task)
    

    def delete_task(self,task) -> Task:
        self.db.delete(task)
        self.db.commit()
        return task
