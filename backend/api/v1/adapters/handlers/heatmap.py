from fastapi import APIRouter, status, Query
from typing import Annotated
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from application.interactors import CreateHeatMapInteractor
from ..schemas import CreateHeatMapIn, CreateHeatMapOut, GetHeatMapUnloadLinkIn, GetHeatMapUnloadLinkOut
from ..responses_descriptions import common_responses, heat_map_responses
from application import dto

router = APIRouter(prefix='/user/videos/heatmap', tags=['HeatMap'], route_class=DishkaRoute)

@router.post('',
             status_code=status.HTTP_201_CREATED,
             description='Create a heatmap',
             responses={
                 status.HTTP_201_CREATED: heat_map_responses['create'][201],
                 status.HTTP_401_UNAUTHORIZED: common_responses[401],
                 status.HTTP_422_UNPROCESSABLE_ENTITY: heat_map_responses['create'][422],
                 status.HTTP_404_NOT_FOUND: heat_map_responses['create'][404],
                 status.HTTP_409_CONFLICT: heat_map_responses['create'][409],
             })
async def create_heatmap(data: CreateHeatMapIn, interactor: FromDishka[CreateHeatMapInteractor]) -> CreateHeatMapOut:
    result = await interactor(dto.CreateHeatMapInDTO(
        video_name=data.video_name
    ))
    return CreateHeatMapOut(upload_link=result.upload_link)

@router.get('/unload_link/{video_name}',
             status_code=status.HTTP_200_OK,
             description='Get heatmap unload link',
             responses={
                 status.HTTP_200_OK: heat_map_responses['get_unload_link'][200],
                 status.HTTP_401_UNAUTHORIZED: common_responses[401],
                 status.HTTP_404_NOT_FOUND: heat_map_responses['get_unload_link'][404],
             })
async def get_heatmap_unload_link(data: Annotated[GetHeatMapUnloadLinkIn, Query()], interactor: FromDishka[CreateHeatMapInteractor]) -> GetHeatMapUnloadLinkOut:
    result = await interactor(dto.GetHeatMapUnloadLinkInDto(
        video_name=data.video_name
    ))
    return GetHeatMapUnloadLinkOut(unload_link=result.upload_link)