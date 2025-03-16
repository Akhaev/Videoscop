from fastapi import APIRouter, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from application.interactors import CreateUserInteractor, UpdateUserInteractor, GetUserInteractor, DeleteUserInteractor
from application import dto
from ..schemas import CreateUser, UpdateUser, GetUser
from ..responses_descriptions import user_responses, common_responses                               


router = APIRouter(prefix='/users', tags=['User'], route_class=DishkaRoute)

@router.post('', status_code=status.HTTP_201_CREATED, name='Create user', 
             summary='Creates a new user',
             responses={status.HTTP_422_UNPROCESSABLE_ENTITY: user_responses[422], 
                        status.HTTP_409_CONFLICT: user_responses[409],
                        status.HTTP_201_CREATED: user_responses[201]}
             )
async def create_user(user: CreateUser, interactor: FromDishka[CreateUserInteractor]) -> dict:
    token = await interactor(dto.CreateUserDTO(**user.model_dump()))
    return {"token": token}


@router.put('', status_code=status.HTTP_200_OK, name='Update user', 
            summary='Updates an existing user',
            responses={status.HTTP_422_UNPROCESSABLE_ENTITY: user_responses[422], 
                       status.HTTP_409_CONFLICT: user_responses[409],
                       status.HTTP_401_UNAUTHORIZED: common_responses[401],
                       status.HTTP_400_BAD_REQUEST: user_responses[400],
                       status.HTTP_404_NOT_FOUND: user_responses[404],
                       status.HTTP_200_OK: user_responses[200]}
            )
async def update_user(user: UpdateUser, interactor: FromDishka[UpdateUserInteractor]) -> dict:
    
    
    await interactor(dto.UpdateUserDto(**user.model_dump()))
    
    return {"message": "User updated successfully"}

@router.get('', status_code=status.HTTP_200_OK, name='Get user', 
            summary='Returns the user data',
            responses={status.HTTP_404_NOT_FOUND: user_responses[404],
                       status.HTTP_401_UNAUTHORIZED: common_responses[401],
                       status.HTTP_200_OK: user_responses[200]}
            )
async def get_user(interactor: FromDishka[GetUserInteractor]) -> GetUser:
    user = await interactor()
    return user

@router.delete('', status_code=status.HTTP_200_OK, name='Delete user', 
               summary='Deletes the user',
               responses={status.HTTP_404_NOT_FOUND: user_responses[404],
                          status.HTTP_401_UNAUTHORIZED: common_responses[401],
                          status.HTTP_200_OK: user_responses[200]}
               )
async def delete_user(interactor: FromDishka[DeleteUserInteractor]) -> dict:
    await interactor()
    return {"message": "User deleted successfully"}

