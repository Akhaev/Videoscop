from dishka import Provider, provide, Scope, from_context, AnyOf
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from config import Config, JWTConfig
from infrastructure.db.database import new_session_maker
from typing import AsyncIterable
from application import interfaces
from infrastructure.db.repositories import UserRepository, VideoRepository, HeatMapRepository
from application.interactors import (CreateUserInteractor, UpdateUserInteractor, GetUserInteractor, 
                                     DeleteUserInteractor, SearchUserVideosInteractor
                                     ,CreateVideoInteractor, CreateHeatMapInteractor)
from uuid import uuid4
from application import validators
from infrastructure.auth import auth
from infrastructure.file_storage import FIleStorage
class FastApiApp(Provider):
    
    config = from_context(provides=Config, scope=Scope.APP)
    
    @provide(scope=Scope.APP)
    async def get_jwt_config(self, config: Config) -> JWTConfig:
        return config.jwtconfig
    
    @provide(scope=Scope.APP)
    async def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        async_session_maker = await new_session_maker(config.postgres)
        return async_session_maker
    
    @provide(scope=Scope.REQUEST)
    async def get_async_session(self, async_sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AnyOf[AsyncSession,interfaces.DBSession]]:
        async with async_sessionmaker() as session:
            yield session
            
    user_repository = provide(UserRepository, scope=Scope.REQUEST, provides=AnyOf[interfaces.UserCreater, interfaces.UserUpdater, interfaces.UserGetter, interfaces.UserDeletter])
    
    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> interfaces.UUIDGenerator:
        return uuid4
    
    create_user_validator = provide(validators.CreateUserValidator, scope=Scope.APP, provides=AnyOf[interfaces.CreateUserValidator])
    
    create_user_authAdd = provide(auth.Auth, scope=Scope.REQUEST, provides=AnyOf[interfaces.AuthAdder])
    
    create_user_interactor = provide(CreateUserInteractor, scope=Scope.REQUEST)
    
    update_user_validator = provide(validators.UpdateUserValidator, scope=Scope.APP, provides=AnyOf[interfaces.UpdateUserValidator])
    
    update_user_authCurrentUserGetter = provide(auth.Auth, scope=Scope.REQUEST, provides=AnyOf[interfaces.AuthCurrentUserGetter])
    
    update_user_interactor = provide(UpdateUserInteractor, scope=Scope.REQUEST)
    
    get_user_interactor = provide(GetUserInteractor, scope=Scope.REQUEST)
    
    delete_user_interactor = provide(DeleteUserInteractor, scope=Scope.REQUEST)
    
    video_repository = provide(VideoRepository, scope=Scope.REQUEST, provides=AnyOf[interfaces.UserVideoSearcher, interfaces.VideoCreater, interfaces.VideoGetter])
    
    search_user_videos_validator = provide(validators.SearchUserVideosValidator, scope=Scope.APP, provides=AnyOf[interfaces.SearchUserVideosValidator])
    search_user_video_interactor = provide(SearchUserVideosInteractor, scope=Scope.REQUEST)
    
    file_storage = provide(FIleStorage, scope=Scope.REQUEST, provides=AnyOf[interfaces.GetFileUploadLink])
    
    create_video_validator = provide(validators.CreateVideoValidator, scope=Scope.APP, provides=AnyOf[interfaces.CreateVideoValidator])
    create_video_interactor = provide(CreateVideoInteractor, scope=Scope.REQUEST)
    
    
    heatmap_repository = provide(HeatMapRepository, scope=Scope.REQUEST, provides=AnyOf[interfaces.HeatMapCreater])
    
    create_heat_map_validator = provide(validators.CreateHeatMapValidator, scope=Scope.APP, provides=AnyOf[interfaces.CreateHeatMapValidator])
    
    create_heat_map_interactor = provide(CreateHeatMapInteractor, scope=Scope.REQUEST)
