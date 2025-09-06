from sqlalchemy import Column, DateTime, Integer, String, func, Enum
from api.user.constants import AuthProvider
from core.models import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(255), unique=True, nullable=False, index=True)
    provider = Column(Enum(AuthProvider), nullable=False, index=True)
    provider_id = Column(String(255), unique=True, nullable=False)

    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    avatar_url = Column(String(500), nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
