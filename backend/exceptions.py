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