from fastapi import APIRouter, HTTPException, status 
from database import SessionDep
from .models import User, UserCreate , Profile
from .service import UserService
from exceptions import UserAlreadyVerifiedError,UserNotFoundError,ServiceError

from .security import current_active_user_dep, get_password_hash
from sqlalchemy.exc import IntegrityError


router = APIRouter(
    prefix="/users",  # Все пути в этом файле будут начинаться с /users
    tags=["Users"]  # Группировка в документации Swagger
)


@router.get("/")
def read_users(session:SessionDep):
    service = UserService(session)
    return service.get_users()



@router.get("/me", response_model=Profile)
def me(my_user : current_active_user_dep):
    return my_user



@router.get("/{user_id}")
def read_user(user_id: int, session: SessionDep):
    service = UserService(session)
    try:
        return service.get_user_profile(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))


@router.delete("/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    service = UserService(session)
    try:
        return service.user_delete(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))



@router.post('/', response_model=User)
def create_user(user_in: UserCreate, session: SessionDep):
    db_user = User.model_validate(user_in,
    update={'hashed_password': get_password_hash(user_in.password)}
    )

    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с такой почтой и таким именем уже есть'
        )
    except Exception as e:
        session.rollback()
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка сервера"
        )

    return db_user

@router.get("/{user_id}/verify")
def verify_user(user_id: int, session: SessionDep):

    service = UserService(session)

    try:
        return service.user_verify(user_id)
    except UserNotFoundError as e:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(e)
        )
    except UserAlreadyVerifiedError as e:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(e)
        )
    except ServiceError:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail='Ошибка сервера'                    
        )




