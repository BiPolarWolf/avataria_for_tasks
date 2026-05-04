from fastapi import APIRouter, HTTPException, status
from database import SessionDep
from .service import TaskService
from users.security import current_active_user_dep
from .models import TaskCreate
from exceptions import TaskIncorrectAuthorError , TaskNotFoundError, ServiceError ,TaskCompletedAlreadyError

router = APIRouter(
    prefix="/tasks",  # Все пути в этом файле будут начинаться с /users
    tags=["Tasks"]  # Группировка в документации Swagger
)


@router.get("/")
def get_tasks(user:current_active_user_dep,session:SessionDep):
    service = TaskService(session)
    return service.get_tasks(user)

@router.post("/create")
def create_task(task_data:TaskCreate,user:current_active_user_dep,session:SessionDep):
    service = TaskService(session)
    return service.create_task(task_data,user)



@router.get("/{task_id}/complete")
def get_task(task_id: int,user:current_active_user_dep,session:SessionDep):
    service = TaskService(session)

    try:
        return service.complete_task(task_id,user)
    except TaskNotFoundError as e:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(e)
        )
    except TaskIncorrectAuthorError as e:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=str(e)
        )
    except TaskCompletedAlreadyError as e:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(e)
        )
    except ServiceError:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail='Ошибка сервера'                    
        )



@router.get("/{task_id}")
def get_task(task_id: int,user:current_active_user_dep,session:SessionDep):
    service = TaskService(session)

    try:
        return service.get_task(task_id,user)
    except TaskNotFoundError as e:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(e)
        )
    except TaskIncorrectAuthorError as e:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=str(e)
        )
    except ServiceError:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail='Ошибка сервера'                    
        )
