from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.base import Settings


engine = create_engine(
    str(Settings.SQLALCHEMY_DATABASE_URI),
    echo=True,  # logs SQL statements
    future=True,  # use SQLAlchemy 2.x style
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
