"""
Создание объекта Limiter для ограничения запросов
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import settings

app_rate_limit = settings.APP_RATE_LIMIT

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[app_rate_limit],
    storage_uri=settings.REDIS_URL
)
