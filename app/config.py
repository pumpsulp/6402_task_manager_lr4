from pydantic_settings import BaseSettings
from pydantic_core import MultiHostUrl
from pydantic import PostgresDsn


class Settings(BaseSettings):
    POSTGRES_SCHEME: str
    POSTGRES_ASYNC_SCHEME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    REDIS_URL: str
    REDIS_PORT: int
    
    APP_RATE_LIMIT: str
    
    FASTAPI_CACHE_EXPIRE_SECONDS: int
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SALT: str
    
    def SQLALCHEMY_DATABASE_URL(self, async_driver: bool = True) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme=self.POSTGRES_ASYNC_SCHEME if async_driver else self.POSTGRES_SCHEME,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        ).unicode_string()
    
    class Config:
        env_file = '.env'


settings = Settings()
