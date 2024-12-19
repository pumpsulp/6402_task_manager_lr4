from app.repo.BaseRepository import BaseRepository
from app.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)
    