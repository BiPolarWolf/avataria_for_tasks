from fastapi import APIRouter, HTTPException, status

from database import SessionDep
from exceptions import (
    ServiceError,
    TagAttachedToNotesError,
    TagIncorrectAuthorError,
    TagNotFoundError,
)
from users.security import current_active_user_dep

from .models import TagCreate, TagUpdate
from .service import TagService


router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)


@router.get("/")
def get_tags(user: current_active_user_dep, session: SessionDep):
    service = TagService(session)
    return service.get_tags(user)


@router.get("/{tag_id}")
def get_tag(tag_id: int, user: current_active_user_dep, session: SessionDep):
    service = TagService(session)

    try:
        return service.get_tag(tag_id, user)
    except TagNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TagIncorrectAuthorError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ServiceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера")


@router.post("/create")
def create_tag(tag_data: TagCreate, user: current_active_user_dep, session: SessionDep):
    service = TagService(session)
    return service.create_tag(tag_data, user)


@router.post("/{tag_id}/update")
def update_tag(tag_id: int, tag_data: TagUpdate, user: current_active_user_dep, session: SessionDep):
    service = TagService(session)

    try:
        return service.update_tag(tag_id, tag_data, user)
    except TagNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TagIncorrectAuthorError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ServiceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера")


@router.post("/{tag_id}/untie")
def untie_tag(tag_id: int, user: current_active_user_dep, session: SessionDep):
    service = TagService(session)

    try:
        return service.untie_tag(tag_id, user)
    except TagNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TagIncorrectAuthorError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ServiceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера")


@router.delete("/{tag_id}/delete")
def delete_tag(tag_id: int, user: current_active_user_dep, session: SessionDep):
    service = TagService(session)

    try:
        return service.delete_tag(tag_id, user)
    except TagNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TagIncorrectAuthorError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except TagAttachedToNotesError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ServiceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера")
