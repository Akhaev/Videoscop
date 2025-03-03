from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.fastapi import inject, FromDishka
router = APIRouter()
@router.get('/api/test')
@inject
def test(session: FromDishka[AsyncSession]) -> str:
    
    return {'message': 's'}