from app.models import Task
from sqlalchemy.ext.asyncio import AsyncSession

from app.repo import TaskRepository
from app.schemas import TaskCreate, TaskUpdate
from app.services import BaseService


class TaskService(BaseService[Task]):
    def __init__(self):
        super().__init__(TaskRepository)
    
    async def create_task(self, db: AsyncSession, task_data: TaskCreate, user_id: int) -> Task:
        """
        Создаёт задачу со значениями task_data и owner_id=user_id
        :param db: Сессия SQLAlchemy
        :param task_data: Данные задачи
        :param user_id: ID пользователя
        :return:
        """
        task_data_dict = task_data.dict()
        task_data_dict["owner_id"] = user_id
        task = await self.create(db, task_data_dict)
        if not task:
            raise ValueError("Task could not be created")
        return task
    
    async def get_task_by_id(self, db: AsyncSession, task_id: int, user_id: int) -> Task:
        """
        Получение задачи пользователя по ID задачи.
        :param db: Сессия SQLAlchemy
        :param task_id: ID задачи
        :param user_id: ID пользователя
        :return:
        """
        task = await self.get(db, filters={"id": task_id, "owner_id": user_id})
        if not task:
            raise ValueError("Not found")
        return task
    
    async def get_tasks_by_user(self, db: AsyncSession, user_id: int) -> list[Task]:
        """
        Получение всех задач пользователя.
        :param db: Сессия SQLAlchemy
        :param user_id: ID пользователя
        :return:
        """
        tasks = await self.repo.get_all(db, filters={"owner_id": user_id})
        if not tasks:
            raise ValueError("Not found")
        return tasks
    
    async def update_task(self, db: AsyncSession, task_id: int, task_data: TaskUpdate, user_id: int) -> Task:
        """
        Обновление данных задачи пользователя.
        :param db: Сессия SQLAlchemy
        :param task_id: ID задачи
        :param task_data: Новые данные задачи
        :param user_id: ID пользователя
        :return:
        """
        updated_task = await self.update(db, filters={"id": task_id, "owner_id": user_id}, obj_in=task_data)
        if not updated_task:
            raise ValueError("Task could not be updated")
        return updated_task
    
    async def delete_task(self, db: AsyncSession, task_id: int, user_id: int) -> Task:
        """
        Удаление задачи пользователя.
        :param db: Сессия SQLAlchemy
        :param task_id: ID задачи
        :param user_id: ID пользователя
        :return:
        """
        task = await self.delete(db, filters={"id": task_id, "owner_id": user_id})
        if not task:
            raise ValueError("Task could not be deleted")
        return task
