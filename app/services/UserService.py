from app.models import User
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.UserRepository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.BaseService import BaseService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(BaseService[User]):
    def __init__(self):
        super().__init__(UserRepository)
    
    async def register_user(self, db: AsyncSession, user_data: UserCreate) -> User:
        """
        Регистрация пользователя
        :param db: сессия SQLAlchemy
        :param user_data: санные пользователя
        :return:
        """
        existing_user = await self.repo.get(db, filters={"email": user_data.email})
        if existing_user:
            raise ValueError(f"User with email {user_data.email} already exists")
        hashed_password = pwd_context.hash(user_data.password)
        
        del user_data.password
        
        user_data_dict = user_data.dict()
        user_data_dict["hashed_password"] = hashed_password
        return await self.create(db, data=user_data_dict)
    
    async def authenticate_user(self, db: AsyncSession, email: str, password: str) -> User:
        """
        Аутентификация пользователя
        :param db: сессия SQLAlchemy
        :param email: адрес пользователя
        :param password: пароль пользователя
        :return:
        """
        user = await self.repo.get(db, filters={"email": email})
        
        if not user:
            raise ValueError(f"User with email {email} not found")
        if not pwd_context.verify(password, user.hashed_password):
            raise ValueError(f"User password is does not match")
        return user
    
