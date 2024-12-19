from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_jwt_token, set_cookie_with_token, invalidate_token
from app.db.database import get_async_db
from app.depends import get_user_service
from app.schemas import UserCreate, User
from app.services.UserService import UserService

router = APIRouter()


@router.post("/register", response_model=User)
async def register_user(
        user_data: UserCreate,
        db: AsyncSession = Depends(get_async_db),
        user_service: UserService = Depends(get_user_service)
):
    """
    POST запрос для регистрации пользователя
    :param user_data: данные пользователя
    :param db: сессия SQLAlchemy
    :param user_service: сервис пользователя
    :return:
    """
    try:
        return await user_service.register_user(db, user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_async_db),
        user_service: UserService = Depends(get_user_service)
):
    """
    POST запрос для авторизации.
    :param response: HTTP-ответ
    :param form_data: OAuth2 форма логина
    :param db: сессия SQLAlchemy
    :param user_service: пользовательский сервис
    :return:
    """
    try:
        user = await user_service.authenticate_user(db, form_data.username, form_data.password)
        
        access_token = await create_jwt_token(data={"sub": str(user.id)})
        await set_cookie_with_token(response, access_token)
        return {"detail": "Login successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/logout")
async def logout(response: Response):
    """
    POST запрос для деавторизации
    :param response: HTTP-ответ
    :return:
    """
    await invalidate_token(response)
    return {"detail": "Successfully logged out"}
