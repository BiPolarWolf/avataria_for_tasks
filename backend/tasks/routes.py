from fastapi import APIRouter
from database import SessionDep
from .service import TaskService
from users.security import current_active_user_dep


router = APIRouter(
    prefix="/tasks",  # Все пути в этом файле будут начинаться с /users
    tags=["Tasks"]  # Группировка в документации Swagger
)


@router.get("/")
def get_tasks(user:current_active_user_dep,session:SessionDep):
    service = TaskService(session)
    return service.get_tasks(user)


@router.get("/{task_id}")
def get_task(task_id: int,session:SessionDep):
    service = TaskService(session)
    return service.get_task(task_id)
