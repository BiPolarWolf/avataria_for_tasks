from fastapi import HTTPException, status


class ServiceError(Exception):
    """Базовое исключение для всех сервисов"""
    pass

class UserNotFoundError(ServiceError):
    """Юзер не найден в базе"""
    pass

class UserAlreadyVerifiedError(ServiceError):
    """Юзер уже прошел верификацию ранее"""
    pass

class AuthException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class TaskNotFoundError(ServiceError):
    """Task не найден в базе"""
    pass

class TaskIncorrectAuthorError(ServiceError):
    """Юзер не является автором Task"""
    pass


class  TaskCompletedAlreadyError(ServiceError):
    """Задача уже выполнена"""
    pass


class TagNotFoundError(ServiceError):
    """Tag не найден в базе"""
    pass


class TagIncorrectAuthorError(ServiceError):
    """Юзер не является автором Tag"""
    pass


class TagAttachedToNotesError(ServiceError):
    """Tag нельзя удалить, пока он привязан к запискам"""
    pass


class NoteNotFoundError(ServiceError):
    """Note не найден в базе"""
    pass


class NoteIncorrectAuthorError(ServiceError):
    """Юзер не является автором Note"""
    pass
