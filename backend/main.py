
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware # Импортируем Middleware
from exceptions import AuthException
from database import create_db_and_tables
from contextlib import asynccontextmanager
from users.routes import router as users_router
from tasks.routes import router as tasks_router
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from users.security import  Token , authenticate_user , create_access_token
from users.models import User
from database import SessionDep


@asynccontextmanager
async def lifespan(app:FastAPI):

    # --- ДЕЙСТВИЯ ПРИ СТАРТЕ ---
    # Создаем таблицы в Postgres, если их еще нет
    create_db_and_tables() 
    print("База данных готова к работе")
    
    yield  # Здесь приложение "живет" и обрабатывает запросы
    
    # --- ДЕЙСТВИЯ ПРИ ОСТАНОВКЕ ---
    # Например, закрытие пула соединений (если нужно)
    print("Приложение выключается")



app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(tasks_router)


# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # В продакшене тут должен быть конкретный адрес
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


@app.post('/token')
def login_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],session: SessionDep) -> Token:


    user : User | None = authenticate_user(session,form_data.username,form_data.password)

    if not user:
        raise AuthException

    access_token = create_access_token(user.username)

    return Token(access_token=access_token,token_type='bearer')


