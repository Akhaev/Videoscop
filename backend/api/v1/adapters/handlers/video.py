from fastapi import APIRouter, status, Query
import datetime
from typing import Annotated
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from application.interactors import SearchUserVideosInteractor, CreateVideoInteractor
from application import dto
from ..schemas import SearchVideoOut, SearchVideoIn, CreateVideoIn
from ..responses_descriptions import common_responses, video_responses

router = APIRouter(prefix='/user/videos', tags=['Video'], route_class=DishkaRoute)

@router.get('/search'
        , status_code=status.HTTP_200_OK,  
        description='Search for a user video by date',
        responses={
        status.HTTP_200_OK: video_responses['search'][200],
        status.HTTP_401_UNAUTHORIZED: common_responses[401],
        status.HTTP_422_UNPROCESSABLE_ENTITY: video_responses['search'][422],
        status.HTTP_404_NOT_FOUND: video_responses['search'][404]
        
        })
async def search_user_video(interactor: FromDishka[SearchUserVideosInteractor], 
                            data: Annotated[SearchVideoIn, Query()]) -> SearchVideoOut | None:
    result = await interactor(dto.SearchUserVideosDTO(date=data.date, count=data.count, cursor=data.cursor))
    return SearchVideoOut(videos=result['videos'], cursor=result['cursor'])

@router.post('',
             status_code=status.HTTP_201_CREATED,
        description='Create a video',
        responses={
        status.HTTP_201_CREATED: video_responses['create'][201],
        status.HTTP_401_UNAUTHORIZED: common_responses[401],
        status.HTTP_422_UNPROCESSABLE_ENTITY: video_responses['create'][422],
        status.HTTP_404_NOT_FOUND: video_responses['create'][404]
        })
async def create_video(interactor: FromDishka[CreateVideoInteractor], video: CreateVideoIn) -> dict:
    upload_link = await interactor(dto.CreateVideoDTO(name=video.name, length_seconds=video.length_seconds, size=video.size))
    return {'upload_link': upload_link}

