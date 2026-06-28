import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware # Импортируем Middleware
from exceptions import AuthException
from database import create_db_and_tables
from contextlib import asynccontextmanager
from users.routes import router as users_router
from users.models import TokenResponse
from tasks.routes import router as tasks_router
from tags.routes import router as tags_router
from notes.routes import router as notes_router
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from users.security import  Token , authenticate_user , create_access_token, create_refresh_token , save_refresh_token_to_db, get_username_from_refresh
from users.models import User
from database import SessionDep
from fastapi import Response 


COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"


@asynccontextmanager
async def lifespan(app:FastAPI):

    # --- ДЕЙСТВИЯ ПРИ СТАРТЕ ---
    # Создаем таблицы в Postgres, если их еще нет
    create_db_and_tables() 
    print("База данных готова к работе ")
    
    yield  # Здесь приложение "живет" и обрабатывает запросы
    
    # --- ДЕЙСТВИЯ ПРИ ОСТАНОВКЕ ---
    # Например, закрытие пула соединений (если нужно)
    print("Приложение выключается")



app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost",
    "http://localhost:8080", # стандартный порт Vue dev-сервера
    "http://localhost:5173", # порт Vite
    "http://your-server-ip",  # IP твоего будущего сервера
    "https://your-domain.com" # Твой домен (если будет)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Разрешаем запросы с этих адресов
    allow_credentials=True,
    allow_methods=["*"], # Разрешаем все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"], # Разрешаем все заголовки
)



app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(tags_router)
app.include_router(notes_router)


# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,    
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {'hello_world':"hello world"}



@app.get("/about")
def read_about():
    return {
        'title' : 'Название проект',
        'description' : "Описание проекта"
    }


@app.post('/refresh')
def refresh_token(username: str = Depends(get_username_from_refresh)) -> Token:
    
    access_token = create_access_token(username)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



@app.post('/logout')
def logout(response: Response):
    # Удаляем куку, перезаписывая её с пустым значением и Max-Age=0
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        samesite="lax", # или "strict" / "none" в зависимости от твоего деплоя
        secure=COOKIE_SECURE     # обязательно для production (HTTPS)
    )
    return {"detail": "Успешно вышел из системы"}




@app.post('/token')
def login_token(response: Response,form_data:Annotated[OAuth2PasswordRequestForm,Depends()],session: SessionDep) -> TokenResponse:

    user : User | None = authenticate_user(session,form_data.username,form_data.password)

    if not user:
        raise AuthException

    access_token = create_access_token(user.username)
    refresh_token,expires_at = create_refresh_token(user.username)
    save_refresh_token_to_db(session,user.id,refresh_token)

    response.set_cookie(
        key="refresh_token", 
        value=refresh_token, 
        httponly=True,   # Огромный плюс к безопасности: JS не видит куку
        secure=COOKIE_SECURE,
        samesite="lax",  # Защита от CSRF
        expires=expires_at
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        'user' : user
    }
