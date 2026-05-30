from fastapi import APIRouter, HTTPException, status

from database import SessionDep
from exceptions import NoteIncorrectAuthorError, NoteNotFoundError, ServiceError, TagNotFoundError
from users.security import current_active_user_dep

from .models import NoteCreate, NoteRead, NoteUpdate
from .service import NoteService


router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.get("/", response_model=list[NoteRead])
def get_notes(user: current_active_user_dep, session: SessionDep):
    service = NoteService(session)
    return service.get_notes(user)


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, user: current_active_user_dep, session: SessionDep):
    service = NoteService(session)

    try:
        return service.get_note(note_id, user)
    except NoteNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NoteIncorrectAuthorError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ServiceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера")


@router.post("/create", response_model=NoteRead)
def create_note(note_data: NoteCreate, user: current_active_user_dep, session: SessionDep):
    service = NoteService(session)

    try:
        return service.create_note(note_data, user)
    except TagNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера")


@router.post("/{note_id}", response_model=NoteRead)
def update_note(note_id: int, note_data: NoteUpdate, user: current_active_user_dep, session: SessionDep):
    service = NoteService(session)

    try:
        return service.update_note(note_id, note_data, user)
    except NoteNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NoteIncorrectAuthorError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except TagNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ServiceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера")


@router.delete("/{note_id}")
def delete_note(note_id: int, user: current_active_user_dep, session: SessionDep):
    service = NoteService(session)

    try:
        return service.delete_note(note_id, user)
    except NoteNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NoteIncorrectAuthorError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ServiceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера")


@router.get("/{note_id}/similar")
def get_similar_notes(note_id: int, user: current_active_user_dep, session: SessionDep):
    service = NoteService(session)

    try:
        return service.get_similar_notes(note_id, user)
    except NoteNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NoteIncorrectAuthorError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ServiceError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера")
