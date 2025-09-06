# SQLAlchemy models
from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, func
from src.api.task.dependencies import TaskStatus
from src.core.models import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    user = ForeignKey("users.id", ondelete="CASCADE", nullable=False)
    content = Column(JSON, nullable=False)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
