from sqlmodel import Session, select
from .models import User

from typing import List

class UserRepository:


    def __init__(self,db : Session):
        self.db = db


    def get_user_by_id(self,user_id : int) -> User | None:
        query = select(User).where(User.id == user_id)
        user = self.db.exec(query).first()
        return user if user else None
    

    def get_users_all(self) -> List[User]:
        query = select(User)
        users = self.db.exec(query).all()
        return users
    

    def __create_or_update_user(self,user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return  user


    def create_user(self,user:User) -> User:
        return self.__create_or_update_user(user)


    def update_user(self,user:User) -> User:
        return self.__create_or_update_user(user)
    

    def delete_user(self,user) -> User:
        self.db.delete(user)
        self.db.commit()
        return user
