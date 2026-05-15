
from datetime import timedelta , datetime, timezone
from typing import Annotated
from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends , HTTPException ,Cookie

from exceptions import AuthException
from .models import RefreshToken, User
from pydantic import BaseModel
from database import SessionDep
from sqlmodel import select
from pwdlib import PasswordHash
from sqlmodel import Session, select

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
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 30
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

def create_refresh_token(username:str):
    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS) 
    to_encode = {'exp': expires_at, 'sub': username}
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return [encoded_jwt,expires_at]


def save_refresh_token_to_db(session: Session, user_id: int, token_string: str):
    # 1. Рассчитываем дату истечения
    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    # 2. Опционально: удаляем старые токены этого пользователя, 
    # чтобы не копить мусор в базе (логика "один пользователь — одно устройство/сессия")
    # Если хочешь разрешить несколько устройств, этот шаг можно пропустить
    statement = select(RefreshToken).where(RefreshToken.user_id == user_id)

    old_tokens = session.exec(statement).all()
    for old_t in old_tokens:
        session.delete(old_t)

    # 3. Создаем объект новой миграции
    db_refresh_token = RefreshToken(
        token=token_string,
        user_id=user_id,
        expires_at=expires_at
    )
    
    # 4. Сохраняем
    session.add(db_refresh_token)
    session.commit()
    session.refresh(db_refresh_token)
    
    return db_refresh_token




def check_valid_refresh_and_give_username(session: Session, refresh_token: str) -> str | None:

    query = select(RefreshToken).where(
        RefreshToken.token == refresh_token,
        RefreshToken.expires_at > datetime.now(timezone.utc),
    )

    refresh_token_object = session.exec(query).first()

    if refresh_token_object :
        return decode_token(refresh_token)


  
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



def decode_token(token: str) -> str | None:
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
    username = decode_token(token)
        
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



def get_username_from_refresh(
    session: SessionDep, 
    refresh_token: Annotated[str | None, Cookie()] = None
) -> str:
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    
    username = check_valid_refresh_and_give_username(session, refresh_token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
        
    return username
