from .repository import UserRepository
from sqlmodel import Session
from exceptions import UserNotFoundError, UserAlreadyVerifiedError
from .models import User
class UserService:
    def __init__(self,db:Session):
        self.repo = UserRepository(db)

    
    def get_user_profile(self,user_id:int) -> User:
        user = self.repo.get_user_by_id(user_id)

        if user is None : 
            raise ValueError('Пользователь не найден')
        
        return user
    

    def user_delete(self,user_id:int):
        user = self.repo.get_user_by_id(user_id)
        if user is None : 
            raise ValueError('Пользователь не найден')
        
        return self.repo.delete_user(user)
    


    def get_users(self):
        users = self.repo.get_users_all()
        return users
    

    def user_verify(self,user_id:int) -> User:

        user = self.repo.get_user_by_id(user_id)

        if user is None:
            raise UserNotFoundError(f'Пользователь с ID {user_id} не найден')
        
        if user.is_verified is True:
            raise UserAlreadyVerifiedError("Пользователь уже верифицирован")
        
        user.is_verified = True

        user_updated = self.repo.update_user(user)

        return user_updated