# FastAPI routes

from fastapi import APIRouter, Depends

from src.core.db import get_db


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get()
async def list_tasks(Session=Depends(get_db)):
    pass
