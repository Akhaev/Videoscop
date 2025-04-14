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

    async def __call__(self, user_dto: dto.CreateUserInDTO) -> dto.CreateUserOutDTO:
        self.validator.validate(user_dto)
        uuid = str(self.uuid_generator())
        
        user_entity = entities.User(
            uuid=uuid,
            login=user_dto.login,
            email=user_dto.email,
            password=user_dto.password
        )
        
        await self.repository.create(user_entity)
        token = self.auth.add(user_entity.uuid)
        await self.db_session.commit()
        return dto.CreateUserOutDTO(token=token)
        
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
    
    async def __call__(self, user_dto: dto.UpdateUserInDTO) -> dto.UpdateUserOutDTO:
        user_uuid = self.auth.get_current_user()
        
        if user_uuid is None:
            raise exceptions.UnAuthorizedError()
        
        if user_dto.current_password is None and (user_dto.email or user_dto.password):
            raise ValueError('requires an up-to-date password to update password or email')
        
        self.validator.validate(user_dto)
        update_fields = {key: value for key, value in asdict(user_dto).items() if value is not None and key != 'current_password'}
        await self.repository.update(user_uuid, update_fields)
        
        await self.db_session.commit()
        return dto.UpdateUserOutDTO(message="User updated successfully")
        

class GetUserInteractor:
    def __init__(self, repository: interfaces.UserGetter, 
                 auth: interfaces.AuthCurrentUserGetter,
                 db_session: interfaces.DBSession) -> None:
        self.repository = repository
        self.auth = auth
        self.db_session = db_session
        
    async def __call__(self) -> dto.GetUserOutDTO:
        user_uuid = self.auth.get_current_user()
        
        if user_uuid is None:
            raise exceptions.UnAuthorizedError()
        
        user_entity = await self.repository.get(user_uuid)
        
        return dto.GetUserOutDTO(login=user_entity.login, email=user_entity.email)

class DeleteUserInteractor:
    def __init__(self, repository: interfaces.UserDeletter, 
                 auth: interfaces.AuthCurrentUserGetter,
                 db_session: interfaces.DBSession) -> None:
        self.repository = repository
        self.auth = auth
        self.db_session = db_session
        
    async def __call__(self) -> dto.DeleteUserOutDTO:
        user_uuid = self.auth.get_current_user()
        
        if user_uuid is None:
            raise exceptions.UnAuthorizedError()
        
        await self.repository.delete(user_uuid)
        
        await self.db_session.commit()
        return dto.DeleteUserOutDTO(message="User deleted successfully")

class SearchUserVideosInteractor:
    def __init__(self, repository: interfaces.UserVideoSearcher, 
                 auth: interfaces.AuthCurrentUserGetter,
                 db_session: interfaces.DBSession,
                 validator: interfaces.SearchUserVideosValidator) -> None:
        self.repository = repository
        self.auth = auth
        self.db_session = db_session
        self.validator = validator
    
    async def __call__(self, search_dto: dto.SearchUserVideosInDTO) -> dto.SearchUserVideosOutDTO:
        user_uuid = self.auth.get_current_user()
        
        if user_uuid is None:
            raise exceptions.UnAuthorizedError()
        
        self.validator.validate(search_dto.count, search_dto.date)
        
        result = await self.repository.search(user_uuid, search_dto.date, search_dto.count, search_dto.cursor)
        
        if result is None:
            return dto.SearchUserVideosOutDTO(videos=[], cursor=None)
        
        return dto.SearchUserVideosOutDTO(videos=result['videos'], cursor=result['cursor'])
    
class CreateVideoInteractor:
    def __init__(self, repository: interfaces.VideoCreater, 
                 db_session: interfaces.DBSession,
                 uuid_generator: interfaces.UUIDGenerator,
                 validator: interfaces.CreateVideoValidator, 
                 auth: interfaces.AuthCurrentUserGetter,
                 file_storage: interfaces.GetFileUploadLink) -> None:
        self.repository = repository
        self.db_session = db_session
        self.uuid_generator = uuid_generator
        self.validator = validator
        self.auth = auth
        self.file_storage = file_storage
        
    async def __call__(self, video_dto: dto.CreateVideoInDTO) -> dto.CreateVideoOutDTO:
        uuid = str(self.uuid_generator())
        author_uuid = self.auth.get_current_user()
        
        if author_uuid is None:
            raise exceptions.UnAuthorizedError()
        
        self.validator.validate(video_dto)
        
        video_entity = entities.Video(
            uuid=uuid,
            name=video_dto.name,
            author_uuid=author_uuid,
            length_seconds=video_dto.length_seconds,
            size=video_dto.size,
            uploaded_at=datetime.date.today(),
        )
        
        await self.repository.create(video_entity)
        
        await self.db_session.commit()
        
        upload_link = await self.file_storage.get_upload_link(file_type='video', file_name=video_dto.name)
        
        return dto.CreateVideoOutDTO(upload_link=upload_link)

class CreateHeatMapInteractor:
    def __init__(self, repository: interfaces.HeatMapCreater,
                 video_repository: interfaces.VideoGetter, 
                 db_session: interfaces.DBSession,
                 uuid_generator: interfaces.UUIDGenerator,
                 auth: interfaces.AuthCurrentUserGetter,
                 file_storage: interfaces.GetFileUploadLink,
                 validator: interfaces.CreateHeatMapValidator) -> None:
        
        self.repository = repository
        self.db_session = db_session
        self.uuid_generator = uuid_generator
        self.auth = auth
        self.file_storage = file_storage
        self.video_repository = video_repository
        self.validator = validator
        
    async def __call__(self, heatmap_dto: dto.CreateHeatMapInDTO) -> dto.CreateHeatMapOutDTO:
        self.validator.validate(heatmap_dto.video_name)
        uuid = str(self.uuid_generator())
        user_uuid = self.auth.get_current_user()
        
        if user_uuid is None:
            raise exceptions.UnAuthorizedError('User not found')    
        
        video = await self.video_repository.get_by_author_and_name(user_uuid, heatmap_dto.video_name)
        
        heat_map_entity = entities.HeatMap(
            uuid=uuid,
            video_uuid=video.uuid
        )
        
        await self.repository.create(heat_map_entity)
        await self.db_session.commit()
        
        upload_link = await self.file_storage.get_upload_link(file_type='heatmap',file_name=heatmap_dto.video_name)
        return dto.CreateHeatMapOutDTO(upload_link=upload_link)

class GetVideoUnloadLinkInteractor:
    def __init__(self, file_storage: interfaces.GetFileUnloadLink,
                 auth: interfaces.AuthCurrentUserGetter,
                 repository: interfaces.VideoGetter,
                 validator: interfaces.GetVideoUnloadLinkValidator) -> None:
        self.file_storage = file_storage
        self.auth = auth
        self.repository = repository
        self.validator = validator
        
    async def __call__(self, video_dto: dto.GetVideoUnloadLinkInDto) -> dto.GetVideoUnloadLinkOutDTO:
        user_uuid = self.auth.get_current_user()
        
        if user_uuid is None:
            raise exceptions.UnAuthorizedError()
        
        self.validator.validate(video_dto)
        _ = await self.repository.get_by_author_and_name(user_uuid, video_dto.video_name)
        
        unload_link = await self.file_storage.get_unload_link(file_type='video', file_name=video_dto.video_name)
        
        return dto.GetVideoUnloadLinkOutDTO(unload_link=unload_link)
    
class GetHeatMapUnloadLinkInteractor:
    def __init__(self, file_storage: interfaces.GetFileUnloadLink,
                 auth: interfaces.AuthCurrentUserGetter,
                 repository: interfaces.HeatMapGetter,
                 validator: interfaces.GetHeatMapUnloadLinkValidator) -> None:
        self.file_storage = file_storage
        self.auth = auth
        self.repository = repository
        self.validator = validator
        
    async def __call__(self, heatmap_dto: dto.GetHeatMapUnloadLinkInDto) -> dto.GetHeatMapUnloadLinkOutDTO:
        user_uuid = self.auth.get_current_user()
        
        if user_uuid is None:
            raise exceptions.UnAuthorizedError()
        
        self.validator.validate(heatmap_dto)
        _ = await self.repository.get_by_author_and_name(user_uuid, heatmap_dto.video_name)
        
        unload_link = await self.file_storage.get_unload_link(file_type='heatmap', file_name=heatmap_dto.video_name)
        
        return dto.GetHeatMapUnloadLinkOutDTO(unload_link=unload_link)

class GenerateUserTokenInteractor:
    def __init__(self, auth: interfaces.AuthAdder,
                 repository: interfaces.UserGetterByLoginPassword, 
                 validator: interfaces.GenerateUserTokenValidator,):
        self.auth = auth
        self.repository = repository
        self.validator = validator
    async def __call__(self, user_dto: dto.GenerateUserTokenInDTO) -> dto.GenerateUserTokenOutDTO:
        self.validator.validate(user_dto)
        user_entity = await self.repository.get_by_login_password(user_dto.login, user_dto.password)

        
        token = self.auth.add(user_entity.uuid)
        return dto.GenerateUserTokenOutDTO(token=token)