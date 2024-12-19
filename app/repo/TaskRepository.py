from app.models import Task
from app.repo.BaseRepository import BaseRepository


class TaskRepository(BaseRepository[Task]):
    def __init__(self) -> None:
        super().__init__(Task)
