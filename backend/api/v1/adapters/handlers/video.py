from fastapi import APIRouter, status, Query
from typing import Annotated
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from application.interactors import SearchUserVideosInteractor, CreateVideoInteractor, GetVideoUnloadLinkInteractor
from ..schemas import SearchVideoOut, SearchVideoIn, CreateVideoIn, CreateVideoOut, GetVideoUnloadLinkIn, GetVideoUnloadLinkOut
from ..responses_descriptions import common_responses, video_responses
from application import dto

router = APIRouter(prefix='/users/me/videos', tags=['Video'], route_class=DishkaRoute)

@router.get('/search',
            status_code=status.HTTP_200_OK,
            description='Search for a user video by date',
            responses={
                status.HTTP_200_OK: video_responses['search'][200],
                status.HTTP_401_UNAUTHORIZED: common_responses[401],
                status.HTTP_422_UNPROCESSABLE_ENTITY: video_responses['search'][422],
                status.HTTP_404_NOT_FOUND: video_responses['search'][404]
            })
async def search_user_video(data: Annotated[SearchVideoIn, Query()], interactor: FromDishka[SearchUserVideosInteractor]) -> dict:
    result = await interactor(dto.SearchUserVideosInDTO(
        date=data.date,
        count=data.count,
        cursor=data.cursor
    ))
    return {"videos": result.videos, "cursor": result.cursor}


@router.post('',
             status_code=status.HTTP_201_CREATED,
             description='Create a video',
             responses={
                 status.HTTP_201_CREATED: video_responses['create'][201],
                 status.HTTP_401_UNAUTHORIZED: common_responses[401],
                 status.HTTP_422_UNPROCESSABLE_ENTITY: video_responses['create'][422],
                 status.HTTP_404_NOT_FOUND: video_responses['create'][404],
                 status.HTTP_409_CONFLICT: video_responses['create'][409]
             })
async def create_video(video: CreateVideoIn, interactor: FromDishka[CreateVideoInteractor]) -> dict:
    result = await interactor(dto.CreateVideoInDTO(
        name=video.name,
        length_seconds=video.length_seconds,
        size=video.size
    ))
    return {"upload_link": result.upload_link}


@router.get('/unload_link',
            status_code=status.HTTP_200_OK,
            description='Get video unload link',
            responses={
                status.HTTP_200_OK: video_responses['get_unload_link'][200],
                status.HTTP_401_UNAUTHORIZED: common_responses[401],
                status.HTTP_404_NOT_FOUND: video_responses['get_unload_link'][404],
                status.HTTP_422_UNPROCESSABLE_ENTITY: video_responses['get_unload_link'][422]
            })
async def get_video_unload_link(data: Annotated[GetVideoUnloadLinkIn, Query()], interactor: FromDishka[GetVideoUnloadLinkInteractor]) -> dict:
    result = await interactor(dto.GetVideoUnloadLinkInDto(
        video_name=data.name
    ))
    return {"unload_link": result.unload_link}