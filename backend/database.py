
from pathlib import Path
from typing import Annotated
from fastapi import Depends
from sqlmodel import  SQLModel, Session, create_engine

BASE_DIR = Path(__file__).resolve().parent
sqlite_file_path = BASE_DIR / "database.db"
sqlite_url = f"sqlite:///{sqlite_file_path}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Параметр check_same_thread=False позволяет FastAPI использовать одну и ту же базу данных SQLite в разных потоках.
#  Это необходимо, так как один запрос может использовать больше одного потока (например, в зависимостях).


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)



    # Code above omitted 👆

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

# Code below omitted 👇
