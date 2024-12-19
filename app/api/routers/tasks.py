from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.security import get_current_user_id
from app.db.database import get_async_db
from app.depends import get_task_service
from app.schemas import TaskCreate, TaskUpdate, TaskOut
from app.services import TaskService

cache_ttl = settings.FASTAPI_CACHE_EXPIRE_SECONDS

router = APIRouter()


@router.post("/tasks", response_model=TaskOut)
async def create_task(
        task_data: TaskCreate,
        db: AsyncSession = Depends(get_async_db),
        task_service: TaskService = Depends(get_task_service),
        user_id: int = Depends(get_current_user_id)
):
    """
    POST запрос создания новой задачи.
    :param task_data: данные в виде схемы
    :param db: сессия SQLAlchemy
    :param task_service: сервис задач
    :param user_id: ID текущего пользователя
    :return:
    """
    try:
        return await task_service.create_task(db, task_data, user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tasks", response_model=list[TaskOut])
@cache(expire=cache_ttl)
async def get_tasks(
        db: AsyncSession = Depends(get_async_db),
        task_service: TaskService = Depends(get_task_service),
        user_id: int = Depends(get_current_user_id)
):
    """
    GET запрос получения списка задач.
    :param db: сессия SQLAlchemy
    :param task_service: сервис задач
    :param user_id: ID текущего пользователя
    :return:
    """
    try:
        return await task_service.get_tasks_by_user(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tasks/{task_id}", response_model=TaskOut)
@cache(expire=cache_ttl)
async def get_task(
        task_id: int,
        db: AsyncSession = Depends(get_async_db),
        task_service: TaskService = Depends(get_task_service),
        user_id: int = Depends(get_current_user_id)
):
    """
    GET запрос получения задачи по ID.
    :param task_id: ID задачи
    :param db: сессия SQLAlchemy
    :param task_service: сервис задач
    :param user_id: ID текущего пользователя
    :return:
    """
    try:
        return await task_service.get_task_by_id(db, task_id, user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/tasks/{task_id}", response_model=TaskOut)
async def update_task(
        task_id: int,
        task_data: TaskUpdate,
        db: AsyncSession = Depends(get_async_db),
        task_service: TaskService = Depends(get_task_service),
        user_id: int = Depends(get_current_user_id)
):
    """
    PUT запрос обновления задачи.
    :param task_id: ID задачи
    :param task_data: данные задачи в виде схемы
    :param db: сессия SQLAlchemy
    :param task_service: сервис задач
    :param user_id: ID текущего пользователя
    :return:
    """
    try:
        task = await task_service.update_task(db, task_id, task_data, user_id)
        return task
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/tasks/{task_id}")
async def delete_task(
        task_id: int,
        db: AsyncSession = Depends(get_async_db),
        task_service: TaskService = Depends(get_task_service),
        user_id: int = Depends(get_current_user_id)
):
    """
    DELETE запрос удаления задачи.
    :param task_id: ID задачи
    :param db: сессия SQLAlchemy
    :param task_service: сервис задач
    :param user_id: ID текущего пользователя
    :return:
    """
    try:
        await task_service.delete_task(db, task_id, user_id)
        return {"detail": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
