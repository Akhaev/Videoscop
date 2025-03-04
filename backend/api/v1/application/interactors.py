from . import interfaces
from . import dto
from domen import entities

class CreateUserInteractor():
    def __init__(self, user_repository: interfaces.UserCreater, 
                 db_session: interfaces.DBSession, 
                 uuid_generator: interfaces.UUIDGenerator,
                 user_validator: interfaces.CreateUserValidator) -> None:
        
        self.user_repository = user_repository
        self.db_session = db_session
        self.uuid_generator = uuid_generator
        self.user_validator = user_validator
        
    async def __call__(self, user: dto.CreateUserDTO) -> entities.User:
        uuid = str(self.uuid_generator())
        
        message = self.user_validator.validate(user)
        
        if message:
            raise ValueError(message)
        
        user_entity = entities.User(
            uuid = uuid,
            login=user.login,
            name=user.name,
            email=user.email,
            password=user.password
        )
        
        try:
            await self.user_repository.create(user_entity)
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")
        
        await self.db_session.commit()
        
        return user_entity
        

    