
from datetime import timedelta , datetime, timezone
from typing import Annotated
from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends , HTTPException, status

from exceptions import AuthException
from .models import User
from pydantic import BaseModel
from database import SessionDep
from sqlmodel import select
from pwdlib import PasswordHash
from sqlmodel import Session

# Загружаем переменные из .env в окружение
load_dotenv()

# ДЛЯ ХЕШИРОВАНИЯ ПАРОЛЕЙ -------------------------------
password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash('dummypassword')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

# -------------------------------------------------------
# JWT settings ------------------------------------------

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
SECRET_KEY = os.getenv('SECRET_KEY')

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

def create_access_token(username:str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
    to_encode = {'exp': expire, 'sub': username}
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

# ------------------------------------------------------



def authenticate_user(session: Session, username: str, password: str):
    user : User | None = session.exec(select(User).where(User.username == username)).first()
    if not user:
        verify_password(password,DUMMY_HASH)
        return None
    if not verify_password(password,user.hashed_password):
        return None
    return user



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_decode_token(token:str) -> str:
    """ Должен по идее декодировать токен и возвращать юзер id но пока просто возвращает username"""
    return token



def decode_access_token(token: str) -> str | None:
    """ тут будет декодироваться jwt_token с извлечением username """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except (InvalidTokenError, AttributeError):
        return None



def get_current_user(
        token : Annotated[str,Depends(oauth2_scheme)],
        session : SessionDep
) -> User :
    """ Возвращает юзера по текену"""


    # тут будет декодироваться jwt_token с извлечением username
    username = decode_access_token(token)
        
    if username is None:
        raise AuthException

    user: User | None = session.exec(select(User).where(User.username == username)).first()

    if user is None:
        raise AuthException

    return user


def get_current_active_user(current_user : Annotated[User,Depends(get_current_user)]) -> User :
    """ Возвращает юзера по токену с проверкой верификации пользователя """
    if not current_user.is_verified:
        raise HTTPException(status_code=403,detail="Пользователь не верифицирован")
    return current_user

current_active_user_dep = Annotated[User,Depends(get_current_active_user)]


