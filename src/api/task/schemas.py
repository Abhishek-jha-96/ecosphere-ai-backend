# Pydantic models

from datetime import datetime
from pydantic import BaseModel

from src.api.task.dependencies import TaskStatus
from src.api.user.models import User


class TaskCreate(BaseModel):
    content: str


class ListTask(BaseModel):
    id: int
    user: User
    status: TaskStatus
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
