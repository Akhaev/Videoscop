from fastapi import APIRouter
from dishka.integrations.fastapi import inject, FromDishka
from application.interactors import CreateUserInteractor
from .schemas import CreateUser
from application import dto
router = APIRouter(prefix='/users')


@router.post('')
@inject
async def create_user(user: CreateUser, interactor: FromDishka[CreateUserInteractor]) -> CreateUser:
    result = await interactor(dto.CreateUserDTO(**user.model_dump()))
    return result