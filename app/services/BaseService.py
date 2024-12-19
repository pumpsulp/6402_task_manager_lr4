from typing import Type, TypeVar, Generic, Dict, Any
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.repo.BaseRepository import BaseRepository
from app.models.Base import Base

T = TypeVar("T", bound=Base)
R = TypeVar("R", bound=BaseRepository)


class BaseService(Generic[T]):
    def __init__(self, repo: Type[R]):
        self.repo = repo()
    
    async def create(self, db: AsyncSession, data: Dict[str, Any]) -> T:
        return await self.repo.create(db, data=data)
    
    async def get(self, db: AsyncSession, filters: Dict[str, Any]) -> T:
        return await self.repo.get(db, filters=filters)
    
    async def update(self, db: AsyncSession, filters: Dict[str, Any], obj_in: BaseModel) -> T:
        update_data = obj_in.dict(exclude_unset=True)
        return await self.repo.update(db, filters=filters, update_data=update_data)
    
    async def delete(self, db: AsyncSession, filters: Dict[str, Any]) -> T:
        return await self.repo.delete(db, filters=filters)
