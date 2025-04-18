from fastapi import APIRouter, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from application.interactors import CreateUserInteractor, UpdateUserInteractor, GetUserInteractor, DeleteUserInteractor, GenerateUserTokenInteractor
from ..schemas import CreateUserIn, CreateUserOut, UpdateUserIn, UpdateUserOut, GetUserOut, DeleteUserOut, GenerateUserTokenOut, GenerateUserTokenIn
from ..responses_descriptions import user_responses, common_responses                               
from application import dto

router = APIRouter(prefix='/users', tags=['User'], route_class=DishkaRoute)

@router.post('', status_code=status.HTTP_201_CREATED, name='Create user', 
             summary='Creates a new user',
             responses={status.HTTP_422_UNPROCESSABLE_ENTITY: user_responses['create'][422], 
                        status.HTTP_409_CONFLICT: user_responses['create'][409],
                        status.HTTP_201_CREATED: user_responses['create'][201]}
             )
async def create_user(user: CreateUserIn, interactor: FromDishka[CreateUserInteractor]) -> CreateUserOut:
    result = await interactor(dto.CreateUserInDTO(
        login=user.login,
        email=user.email,
        password=user.password
    ))
    return CreateUserOut(token=result.token)


@router.put('/me', status_code=status.HTTP_200_OK, name='Update user', 
            summary='Updates an existing user',
            responses={status.HTTP_422_UNPROCESSABLE_ENTITY: user_responses['update'][422], 
                       status.HTTP_409_CONFLICT: user_responses['update'][409],
                       status.HTTP_401_UNAUTHORIZED: common_responses[401],
                       status.HTTP_400_BAD_REQUEST: user_responses['update'][400],
                       status.HTTP_404_NOT_FOUND: user_responses['update'][404],
                       status.HTTP_200_OK: user_responses['update'][200]}
            )
async def update_user(user: UpdateUserIn, interactor: FromDishka[UpdateUserInteractor]) -> UpdateUserOut:
    await interactor(dto.UpdateUserInDTO(
        login=user.login,
        email=user.email,
        password=user.password,
        current_password=user.current_password
    ))
    return UpdateUserOut(message="User updated successfully")


@router.get('/me', status_code=status.HTTP_200_OK, name='Get user', 
            summary='Returns the user data',
            responses={status.HTTP_404_NOT_FOUND: user_responses['get'][404],
                       status.HTTP_401_UNAUTHORIZED: common_responses[401],
                       status.HTTP_200_OK: user_responses['get'][200]}
            )
async def get_user(interactor: FromDishka[GetUserInteractor]) -> GetUserOut:
    result = await interactor()
    return GetUserOut(login=result.login, email=result.email)


@router.delete('/me', status_code=status.HTTP_200_OK, name='Delete user', 
               summary='Deletes the user',
               responses={status.HTTP_404_NOT_FOUND: user_responses['delete'][404],
                          status.HTTP_401_UNAUTHORIZED: common_responses[401],
                          status.HTTP_200_OK: user_responses['delete'][200]}
               )
async def delete_user(interactor: FromDishka[DeleteUserInteractor]) -> DeleteUserOut:
    await interactor()
    return DeleteUserOut(message="User deleted successfully")

@router.post('/me/token', status_code=status.HTTP_201_CREATED, name='Generate user token', 
             summary='Generates a new authentication token for the user',
             responses={status.HTTP_422_UNPROCESSABLE_ENTITY: user_responses['generate_token'][422], 
                        status.HTTP_404_NOT_FOUND: user_responses['generate_token'][404],
                        status.HTTP_201_CREATED: user_responses['generate_token'][201]}
             )
async def generate_token(user: GenerateUserTokenIn, interactor: FromDishka[GenerateUserTokenInteractor]) -> GenerateUserTokenOut:
    result = await interactor(dto.GenerateUserTokenInDTO(login=user.login, email=user.email, password=user.password))

    return GenerateUserTokenOut(token=result.token)