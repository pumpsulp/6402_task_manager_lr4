from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.Base import Base


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    
    tasks = relationship("Task", back_populates="owner", cascade="save-update, delete, delete-orphan")
