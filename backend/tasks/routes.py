from fastapi import APIRouter, HTTPException, Query, status
from database import SessionDep
from .service import TaskService
from users.security import current_active_user_dep
from .models import TaskCreate , TaskUpdate , TaskRead
from exceptions import TaskIncorrectAuthorError , TaskNotFoundError, ServiceError ,TaskCompletedAlreadyError, TagNotFoundError

router = APIRouter(
    prefix="/tasks",  # Все пути в этом файле будут начинаться с /users
    tags=["Tasks"]  # Группировка в документации Swagger
)


@router.get("/", response_model=list[TaskRead])
def get_tasks(
    user:current_active_user_dep,
    session:SessionDep,
    search: str | None = Query(default=None),
    tag_ids: list[int] = Query(default=[]),
):
    service = TaskService(session)
    return service.get_tasks(user, search=search, tag_ids=tag_ids)

@router.get("/active", response_model=list[TaskRead])
def get_active_tasks(
    user:current_active_user_dep,
    session:SessionDep,
    search: str | None = Query(default=None),
    tag_ids: list[int] = Query(default=[]),
):
    service = TaskService(session)
    return service.get_tasks(user,'active', search=search, tag_ids=tag_ids)

@router.get("/completed", response_model=list[TaskRead])
def get_completed_tasks(
    user:current_active_user_dep,
    session:SessionDep,
    search: str | None = Query(default=None),
    tag_ids: list[int] = Query(default=[]),
):
    service = TaskService(session)
    return service.get_tasks(user,'completed', search=search, tag_ids=tag_ids)


@router.get('/stats')
def get_tasks_user_stats(user:current_active_user_dep,session:SessionDep):
    service = TaskService(session)
    return service.get_user_tasks_stats(user)


@router.post("/create", response_model=TaskRead)
def create_task(task_data:TaskCreate,user:current_active_user_dep,session:SessionDep):
    service = TaskService(session)
    try:
        return service.create_task(task_data,user)
    except TagNotFoundError as e:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(e)
        )
    except ServiceError:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail='Ошибка сервера'
        )


@router.post('/update', response_model=TaskRead)
def update_task(task_data:TaskUpdate,user:current_active_user_dep,session:SessionDep):
    service = TaskService(session)
    try:
        return service.update_task(task_data,user)
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
    except TagNotFoundError as e:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(e)
        )
    except ServiceError:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail='Ошибка сервера'                    
        )


@router.get("/{task_id}/complete")
def complete_task(task_id: int,user:current_active_user_dep,session:SessionDep):
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


@router.delete("/{task_id}")
def delete_task(task_id: int,user:current_active_user_dep,session:SessionDep):
    service = TaskService(session)

    try:
        return service.task_delete(task_id,user)
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



@router.get("/{task_id}", response_model=TaskRead)
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
