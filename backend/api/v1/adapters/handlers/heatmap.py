from fastapi import APIRouter, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from application.interactors import CreateHeatMapInteractor
from ..responses_descriptions import common_responses, heat_map_responses

router = APIRouter(prefix='/user/videos/heatmaps', tags=['HeatMap'], route_class=DishkaRoute)


@router.post(''
             , status_code=status.HTTP_201_CREATED,  
        description='Create a heatmap',
        responses={
        status.HTTP_201_CREATED: heat_map_responses['create'][201],
        status.HTTP_401_UNAUTHORIZED: common_responses[401],
        status.HTTP_422_UNPROCESSABLE_ENTITY: heat_map_responses['create'][422],
        status.HTTP_404_NOT_FOUND: heat_map_responses['create'][404]
        
        })
async def create_heatmap(interactor: FromDishka[CreateHeatMapInteractor], video_name: str) -> dict:
    link = interactor(video_name)
    return {'upload_link': link}