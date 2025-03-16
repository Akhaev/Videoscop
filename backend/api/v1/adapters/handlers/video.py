from fastapi import APIRouter, status, Query
import datetime
from typing import Annotated
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from application.interactors import SearchUserVideoInteractor
from ..schemas import SearchVideoOut
router = APIRouter(prefix='/videos', tags=['Video'], route_class=DishkaRoute)

@router.get('/search')
async def search_user_video(interactor: FromDishka[SearchUserVideoInteractor], date: Annotated[Query[description='Date of the video'], datetime.date]) -> list[SearchVideoOut]:
    videos = await interactor(date)
    return videos