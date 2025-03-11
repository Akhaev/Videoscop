from . import interfaces
from . import dto
from domen import entities
from . import exceptions

class CreateUserInteractor():
    def __init__(self, user_repository: interfaces.UserCreater, 
                 db_session: interfaces.DBSession, 
                 uuid_generator: interfaces.UUIDGenerator,
                 user_validator: interfaces.CreateUserValidator,
                 auth: interfaces.AuthAdder) -> None:
        
        self.user_repository = user_repository
        self.db_session = db_session
        self.uuid_generator = uuid_generator
        self.user_validator = user_validator
        self.auth = auth
    async def __call__(self, user: dto.CreateUserDTO) -> interfaces.Token:
        
        self.user_validator.validate(user)
        uuid = str(self.uuid_generator())
        
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
        
class UpdateUserInteractor():
    
    def __init__(self,
                 user_repository: interfaces.UserUpdater,  
                 validator: interfaces.UserUpdateValidator,
                 auth: interfaces.AuthCurrentUserGetter) -> None:
        
        self.user_repository = user_repository
        self.validator = validator
        self.auth = auth
    
    def __call__(self, fields: dto.UpdateUserDTO, current_password: str | None = None) -> None:
        user_id = self.auth.get_current_user()
        
        if user_id is None:
            raise exceptions.UnauthorizedError()
        
        if current_password is None and fields['email'] is not None or fields['password'] is not None:
            raise exceptions.UnAuthorizedError()
        
        self.validator()