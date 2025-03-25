from fastapi import APIRouter, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from application.interactors import CreateHeatMapInteractor
from ..schemas import CreateHeatMapIn, CreateHeatMapOut
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
                 status.HTTP_404_NOT_FOUND: heat_map_responses['create'][404]
             })
async def create_heatmap(data: CreateHeatMapIn, interactor: FromDishka[CreateHeatMapInteractor]) -> CreateHeatMapOut:
    result = await interactor(dto.CreateHeatMapInDTO(
        video_name=data.video_name
    ))
    return CreateHeatMapOut(upload_link=result.upload_link)