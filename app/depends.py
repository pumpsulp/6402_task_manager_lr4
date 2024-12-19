"""
Файл внедрения зависимостей
"""
from app.services.TaskService import TaskService
from app.services.UserService import UserService
import redis.asyncio as aioredis
from app.config import settings

redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

user_service = UserService()
task_service = TaskService()


async def get_user_service() -> UserService:
    return user_service


async def get_task_service() -> TaskService:
    return task_service

async def get_redis_client() -> aioredis.Redis:
    return redis_client