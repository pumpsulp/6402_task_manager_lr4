from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.limiter import limiter
from app.api.routers import users, tasks
from app.depends import get_redis_client

app = FastAPI()

app.add_middleware(SlowAPIMiddleware)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.on_event("startup")
async def startup():
    # инициализируем кэш
    FastAPICache.init(RedisBackend(get_redis_client()), prefix="fastapi-cache")
    
    app.include_router(users.router)
    app.include_router(tasks.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Task API"}


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )
