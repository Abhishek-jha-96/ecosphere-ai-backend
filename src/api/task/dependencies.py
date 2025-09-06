# Dependencies

from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    EXPIRED = "expired"
