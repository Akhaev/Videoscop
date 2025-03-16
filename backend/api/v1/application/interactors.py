from . import interfaces
from . import dto
from domen import entities
from . import exceptions
from dataclasses import asdict
import datetime

class CreateUserInteractor:
    def __init__(self, repository: interfaces.UserCreater, 
                 db_session: interfaces.DBSession, 
                 uuid_generator: interfaces.UUIDGenerator,
                 validator: interfaces.CreateUserValidator,
                 auth: interfaces.AuthAdder) -> None:
        
        self.repository = repository
        self.db_session = db_session
        self.uuid_generator = uuid_generator
        self.validator = validator
        self.auth = auth
    async def __call__(self, dto: dto.CreateUserDTO) -> interfaces.Token:
        
        self.validator.validate(dto)
        uuid = str(self.uuid_generator())
        
        user_entity = entities.User(
            uuid = uuid,
            login=dto.login,
            email=dto.email,
            password=dto.password
        )
        
        await self.repository.create(user_entity)
        

        
        token = self.auth.add(user_entity.uuid)
        await self.db_session.commit()
        return token
        
class UpdateUserInteractor:
    
    def __init__(self,
                 repository: interfaces.UserUpdater,  
                 validator: interfaces.UpdateUserValidator,
                 auth: interfaces.AuthCurrentUserGetter,
                 db_session: interfaces.DBSession) -> None:
        
        self.repository = repository
        self.validator = validator
        self.auth = auth
        self.db_session = db_session
    
    async def __call__(self, dto: dto.UpdateUserDto, current_password: str | None = None) -> None:
        user_id = self.auth.get_current_user()
        
        if user_id is None:
            raise exceptions.UnauthorizedError()
        
        if dto.current_password is None and (dto.email is not None or dto.password is not None):
            raise ValueError('requires an up-to-date password to update password or email')
        
        self.validator.validate(dto)
        update_fields = {key: value for key, value in zip(asdict(dto).keys(), asdict(dto).values()) if value is not None or key != 'current_password'}
        del update_fields['current_password']
        await self.repository.update(user_id, update_fields)
        
        await self.db_session.commit()
        

class GetUserInteractor:
    def __init__(self, repository: interfaces.UserGetter, 
                 auth: interfaces.AuthCurrentUserGetter,
                 db_session: interfaces.DBSession) -> None:
        self.repository = repository
        self.auth = auth
        self.db_session = db_session
        
    async def __call__(self) -> entities.User:
        user_id = self.auth.get_current_user()
        
        if user_id is None:
            raise exceptions.UnauthorizedError()
        
        user_entity = await self.repository.get(user_id)
        
        return user_entity

class DeleteUserInteractor:
    def __init__(self, repository: interfaces.UserDeletter, 
                 auth: interfaces.AuthCurrentUserGetter,
                 db_session: interfaces.DBSession) -> None:
        self.repository = repository
        self.auth = auth
        self.db_session = db_session
        
    async def __call__(self):
        user_id = self.auth.get_current_user()
        
        if user_id is None:
            raise exceptions.UnauthorizedError()
        
        await self.repository.delete(user_id)
        
        await self.db_session.commit()

class SearchUserVideoInteractor:
    def __init__(self, repository: interfaces.UserVideoSearcher, 
                 auth: interfaces.AuthCurrentUserGetter,
                 db_session: interfaces.DBSession) -> None:
        self.repository = repository
        self.auth = auth
        self.db_session = db_session
    
    def __call__(self, date: datetime.date) -> list[entities.Video] | None:
        user_id = self.auth.get_current_user()
        
        if user_id is None:
            raise exceptions.UnauthorizedError()
        
        videos = self.repository.search_by_date(user_id, date)
        
        if videos is None:
            return None
        
        return videos