from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import inject, FromDishka
from application.interactors import CreateUserInteractor
from .schemas import CreateUser
from application import dto
from fastapi import status

router = APIRouter(prefix='/users', tags=['User'])

@router.post('', status_code=status.HTTP_201_CREATED, name='Create user', 
             summary='Creates a user with the specified data',
             responses={status.HTTP_422_UNPROCESSABLE_ENTITY: response_422}
             )
@inject
async def create_user(user: CreateUser, interactor: FromDishka[CreateUserInteractor]) -> CreateUser:
    result = await interactor(dto.CreateUserDTO(**user.model_dump()))
    return result


        