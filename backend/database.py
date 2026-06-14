
from typing import Annotated
from fastapi import Depends
from sqlmodel import  SQLModel, Session, create_engine
import os

# 1. Проверяем переменную окружения. Если её нет, берем локальный sqlite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# 2. Маленький нюанс: для SQLite нужен специальный флаг check_same_thread
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)



# Параметр check_same_thread=False позволяет FastAPI использовать одну и ту же базу данных SQLite в разных потоках.
#  Это необходимо, так как один запрос может использовать больше одного потока (например, в зависимостях).


def create_db_and_tables():
    import notes.models  # noqa: F401
    import tags.models  # noqa: F401
    import tasks.models  # noqa: F401
    import users.models  # noqa: F401

    SQLModel.metadata.create_all(engine)



    # Code above omitted 👆

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

# Code below omitted 👇
