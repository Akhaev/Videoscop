from fastapi import APIRouter, status, Query
import datetime
from typing import Annotated
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from application.interactors import SearchUserVideosInteractor
from application import dto
from ..schemas import SearchVideoOut, SearchVideoIn
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
async def search_user_video(interactor: FromDishka[SearchUserVideosInteractor], 
                            data: Annotated[SearchVideoIn, Query()]) -> SearchVideoOut | None:
    result = await interactor(dto.SearchUserVideosDTO(date=data.date, count=data.count, cursor=data.cursor))
    return SearchVideoOut(videos=result['videos'], cursor=result['cursor'])