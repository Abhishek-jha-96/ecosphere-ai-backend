from sqlalchemy import Column, DateTime, Integer, String, func

from core.models import Base


class MyModel(Base):
    __tablename__ = "my_model"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
