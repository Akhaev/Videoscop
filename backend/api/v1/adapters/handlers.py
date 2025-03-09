from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from application.interactors import CreateUserInteractor
from .schemas import CreateUser
from application import dto
from fastapi import status
from .responses_descriptions import response_409, response_422, response_201

router = APIRouter(prefix='/users', tags=['User'], route_class=DishkaRoute)


@router.post('', status_code=status.HTTP_201_CREATED, name='Create user', 
             summary='Creates a new user',
             responses={status.HTTP_422_UNPROCESSABLE_ENTITY: response_422, 
                        status.HTTP_409_CONFLICT: response_409,
                        status.HTTP_201_CREATED: response_201}
             )
async def create_user(user: CreateUser, interactor: FromDishka[CreateUserInteractor]) -> str:
    result = await interactor(dto.CreateUserDTO(**user.model_dump()))
    return result


        