from . import interfaces
from . import dto
from domen import entities

class CreateUserInteractor():
    def __init__(self, user_repository: interfaces.UserCreater, 
                 db_session: interfaces.DBSession, 
                 uuid_generator: interfaces.UUIDGenerator) -> None:
        
        self.user_repository = user_repository
        self.db_session = db_session
    
    def __call__(self, user: dto.CreateUserDTO) -> entities.User:
        user_entity = entities.User(
            login=user.login,
            name=user.name,
            email=user.email,
            password=user.password
        )
        
        self.user_repository.create_user(user_entity)
        self.db_session.commit()
        
        return user_entity
        

    