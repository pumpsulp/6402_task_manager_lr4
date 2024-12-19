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


async def set_cookie_with_token(response: Response, token: str):
    """
    Добавление в Response Cookie с JWT-токеном
    :param response: Response (HTTP-ответ)
    :param token: зашифрованный JWT-токен
    :return:
    """
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,  # Защита от CRSF
        max_age=ACCESS_TOKEN_EXPIRE_SECONDS,
        expires=ACCESS_TOKEN_EXPIRE_SECONDS,
        samesite="lax",
        secure=True
    )


def get_user_id_from_token(payload: dict) -> int:
    """
    Получает user_id из полезной нагрузки токена (payload).
    Если user_id отсутствует, бросает HTTPException с 401 статусом.
    :param payload: полезная нагрузка
    """
    user_id: str = payload.get("sub")
    if user_id is None:
        raise not_authorized_exception
    return int(user_id)


async def get_token_from_cookie(request: Request):
    """
    Получение зашифрованного JWT-токена из Cookie HTTP-запроса
    :param request: HTTP-запрос
    :return:
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Can't get token")
    return token


async def get_current_user_id(request: Request) -> int:
    """
    Основная функция для получения текущего пользователя из Cookie.
    Декодирует токен JWT и возвращает user_id.
    :param request: HTTP-запрос
    """
    try:
        token = request.cookies.get("access_token")
        if token is None:
            raise not_authorized_exception
    
        payload = decode_jwt_token(token)
        user_id = get_user_id_from_token(payload)
        return user_id
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


async def invalidate_token(response: Response):
    """
    Инвалидизация JWT-токена
    :param response: HTTP-ответ
    :return:
    """
    response.delete_cookie("access_token")
