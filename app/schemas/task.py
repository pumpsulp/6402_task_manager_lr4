from typing import Optional, List
from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: Optional[str]


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    is_completed: Optional[bool] = False


class TaskResponse(TaskBase):
    id: int
    is_completed: bool
    owner_id: int
    
    class Config:
        orm_mode = True


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    
    class Config:
        orm_mode = True


class TaskOut(TaskBase):
    id: int
    owner_id: int
    
    class Config:
        orm_mode = True

