from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config import settings

# TODO: параметры engine стоит хранить в переменных среды
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL(async_driver=True),
    pool_size=10,  # максимальное количество постоянных соединений
    max_overflow=20,  # дополнительные соединения сверх pool_size
    pool_timeout=30,  # таймаут ожидания соединения
    pool_recycle=1800,  # время перезагрузки соединений
    echo=True  # логирование sql query
)

# Создаем фабрику асинхронных сессий
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)


# TODO: инициализировать сессию другим образом и переместить в depends.py
async def get_async_db():
    async with SessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise e
        finally:
            await db.close()
