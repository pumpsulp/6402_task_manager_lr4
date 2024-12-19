from typing import Type, TypeVar, Dict, Any, Generic, List, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.Base import Base

T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    """
    Базовый асинхронный репозиторий
    """
    
    def __init__(self, model: Type[T]):
        self.model = model
    
    async def create(self, db: AsyncSession, data: Dict[str, Any]) -> T:
        """
        Создание записи в таблице
        :param db: сессия SQLAlchemy
        :param data: значения полей (данные)
        :return:
        """
        db_obj = self.model(**data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def get(self, db: AsyncSession, filters: Dict[str, Any]) -> T:
        """
        Получение записи в таблице с определенными значениями.
        
        Внимание!
        При наличии нескольких записей, возвращается первая.
        Для получения всех записей следует пользоваться get_all.
        :param db: сессия SQLAlchemy
        :param filters: значения полей (фильтр)
        :return:
        """
        query = select(self.model)
        for key, value in filters.items():
            query = query.filter(getattr(self.model, key) == value)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def update(self, db: AsyncSession, filters: Dict[str, Any], update_data: Dict[str, Any]) -> Union[T, None]:
        """
        Обновление записи в таблице с определенными значениями.
        :param db: сессия SQLAlchemy
        :param filters: значения полей (фильтр)
        :param update_data: новые значения полей
        :return:
        """
        db_obj = await self.get(db, filters)
        if not db_obj:
            return None
        
        for key, value in update_data.items():
            setattr(db_obj, key, value)
        
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, filters: Dict[str, Any]) -> Union[T, None]:
        """
        Удаление записи в таблице с определенными значениями.
        :param db: сессия SQLAlchemy
        :param filters: значения полей (фильтр)
        :return:
        """
        db_obj = await self.get(db, filters)
        if not db_obj:
            return None
        
        await db.delete(db_obj)
        await db.commit()
        return db_obj
        
    async def get_all(self, db: AsyncSession, filters: Dict[str, Any]) -> List[T]:
        """
        Получение всех записей в таблице с определенными значениями.
        :param db: сессия SQLAlchemy
        :param filters: значения полей (фильтр)
        :return:
        """
        query = select(self.model)
        for key, value in filters.items():
            query = query.filter(getattr(self.model, key) == value)
        result = await db.execute(query)
        tasks = result.scalars().all()
        return list(tasks)
