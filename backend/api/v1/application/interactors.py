from . import interfaces
from . import dto
from domen import entities
from . import exceptions
from dataclasses import asdict
from datetime import datetime

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
    
    async def __call__(self, dto: dto.UpdateUserDto) -> None:
        user_uuid = self.auth.get_current_user()
        
        if user_uuid is None:
            raise exceptions.UnauthorizedError()
        
        if dto.current_password is None and (dto.email is not None or dto.password is not None):
            raise ValueError('requires an up-to-date password to update password or email')
        
        self.validator.validate(dto)
        update_fields = {key: value for key, value in zip(asdict(dto).keys(), asdict(dto).values()) if value is not None or key != 'current_password'}
        del update_fields['current_password']
        await self.repository.update(user_uuid, update_fields)
        
        await self.db_session.commit()
        

class GetUserInteractor:
    def __init__(self, repository: interfaces.UserGetter, 
                 auth: interfaces.AuthCurrentUserGetter,
                 db_session: interfaces.DBSession) -> None:
        self.repository = repository
        self.auth = auth
        self.db_session = db_session
        
    async def __call__(self) -> entities.User:
        user_uuid = self.auth.get_current_user()
        
        if user_uuid is None:
            raise exceptions.UnauthorizedError()
        
        user_entity = await self.repository.get(user_uuid)
        
        return user_entity

class DeleteUserInteractor:
    def __init__(self, repository: interfaces.UserDeletter, 
                 auth: interfaces.AuthCurrentUserGetter,
                 db_session: interfaces.DBSession) -> None:
        self.repository = repository
        self.auth = auth
        self.db_session = db_session
        
    async def __call__(self):
        user_uuid = self.auth.get_current_user()
        
        if user_uuid is None:
            raise exceptions.UnauthorizedError()
        
        await self.repository.delete(user_uuid)
        
        await self.db_session.commit()

class SearchUserVideosInteractor:
    def __init__(self, repository: interfaces.UserVideoSearcher, 
                 auth: interfaces.AuthCurrentUserGetter,
                 db_session: interfaces.DBSession,
                 validator: interfaces.SearchUserVideosValidator) -> None:
        self.repository = repository
        self.auth = auth
        self.db_session = db_session
        self.validator = validator
    
    async def __call__(self, dto: dto.SearchUserVideosDTO) -> dict['videos': list[entities.Video], 'cursor': str | None]:
        user_uuid = self.auth.get_current_user()
        
        if user_uuid is None:
            raise exceptions.UnauthorizedError()
        
        self.validator.validate(dto.count, dto.date)
        
        result = await self.repository.search(user_uuid, dto.date, dto.count, dto.cursor)
        
        if result is None:
            return {"videos": [], "cursor": None}
        
        return result
    
class CreateVideoInteractor:
    def __init__(self, repository: interfaces.VideoCreater, 
                 db_session: interfaces.DBSession,
                 uuid_generator: interfaces.UUIDGenerator,
                 validator: interfaces.CreateVideoValidator, 
                 auth: interfaces.AuthCurrentUserGetter,) -> None:
        self.repository = repository
        self.db_session = db_session
        self.uuid_generator = uuid_generator
        self.validator = validator
        self.auth = auth
        
    async def __call__(self, dto: dto.CreateVideoDTO) -> None:
        uuid = str(self.uuid_generator())
        user_uuid = self.auth.get_current_user()
        self.validator.validate(dto)
        
        video_entity = entities.Video(
            uuid = uuid,
            name=dto.name,
            author_id=user_uuid,
            length_seconds=dto.length_seconds,
            size=dto.size,
            uploaded_at=datetime.date(),
        )
        
        await self.repository.create(video_entity)
        
        await self.db_session.commit()