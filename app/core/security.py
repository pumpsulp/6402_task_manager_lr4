from datetime import datetime, timedelta
from typing import Dict, Union

from fastapi import HTTPException, Response, Request
from jose import jwt
from passlib.context import CryptContext

from app.config import settings

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

ACCESS_TOKEN_EXPIRE = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
ACCESS_TOKEN_EXPIRE_SECONDS = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES).seconds

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

not_authorized_exception = HTTPException(
    status_code=403,
    detail="Not authorized"
)


def hash_password(password):
    """
    Хэширование пароля
    :param password: пароль
    :return: хэшированный пароль
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    Верификация хэшированного пароля
    :param plain_password: пароль
    :param hashed_password: хэшированный пароль
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


async def create_jwt_token(data: Dict[str, Union[str, int, datetime]]) -> str:
    """
    Создание JWT-токена
    :param data: данные JWT
    :return: JWT-токен
    """
    to_encode = data.copy()
    expire = datetime.now() + ACCESS_TOKEN_EXPIRE
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_jwt_token(token: str) -> dict:
    """
    Декодирование JWT-токена, используя SECRET_KEY и ALGORITHM.
    :param token: JWT-токен
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload