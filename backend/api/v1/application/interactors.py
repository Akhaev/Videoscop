from . import interfaces
from . import dto
from domen import entities

class CreateUserInteractor():
    def __init__(self, user_repository: interfaces.UserCreater, 
                 db_session: interfaces.DBSession, 
                 uuid_generator: interfaces.UUIDGenerator,
                 user_validator: interfaces.CreateUserValidator,
                 auth: interfaces.AuthAdd) -> None:
        
        self.user_repository = user_repository
        self.db_session = db_session
        self.uuid_generator = uuid_generator
        self.user_validator = user_validator
        self.auth = auth
    async def __call__(self, user: dto.CreateUserDTO) -> interfaces.Token:
        uuid = str(self.uuid_generator())
        
        self.user_validator.validate(user)
        
        
        user_entity = entities.User(
            uuid = uuid,
            login=user.login,
            name=user.name,
            email=user.email,
            password=user.password
        )
        
        await self.user_repository.create(user_entity)
        

        
        token = self.auth.add(user_entity.uuid)
        await self.db_session.commit()
        return token
        
