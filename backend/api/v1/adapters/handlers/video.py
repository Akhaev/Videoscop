from fastapi import APIRouter, status, Query
import datetime
from typing import Annotated
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from application.interactors import SearchUserVideosInteractor
from ..schemas import SearchVideoOut
from ..responses_descriptions import common_responses, video_responses
router = APIRouter(prefix='/videos', tags=['Video'], route_class=DishkaRoute)

@router.get('/search'
        , status_code=status.HTTP_200_OK,  
        description='Search for a user video by date',
        responses={
        status.HTTP_200_OK: video_responses['search'][200],
        status.HTTP_401_UNAUTHORIZED: common_responses[401],
        status.HTTP_422_UNPROCESSABLE_ENTITY: video_responses['search'][422],
        
        })
async def search_user_video(interactor: FromDishka[SearchUserVideosInteractor], date: Annotated[datetime.date, Query(description='Date of the video')] | None = None) -> SearchVideoOut | None:
    videos = await interactor(date)
    return videos