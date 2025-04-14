from dishka import Provider, provide, Scope, from_context, AnyOf
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from config import Config, JWTConfig, MinioConfig
from infrastructure.db.database import new_session_maker
from typing import AsyncIterable
from application import interfaces
from infrastructure.db.repositories import UserRepository, VideoRepository, HeatMapRepository
from application.interactors import (CreateUserInteractor, UpdateUserInteractor, GetUserInteractor, 
                                     DeleteUserInteractor, SearchUserVideosInteractor
                                     ,CreateVideoInteractor, CreateHeatMapInteractor, 
                                     GetHeatMapUnloadLinkInteractor, GetVideoUnloadLinkInteractor,
                                     GenerateUserTokenInteractor
                                     )
from uuid import uuid4
from application import validators
from infrastructure.auth import auth
from infrastructure.file_storage import file_storage
from minio import Minio

class FastApiApp(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_jwt_config(self, config: Config) -> JWTConfig:
        return config.jwt

    @provide(scope=Scope.APP)
    async def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        async_session_maker = await new_session_maker(config.postgres)
        return async_session_maker

    @provide(scope=Scope.APP)
    async def get_minio_client(self, config: Config) -> Minio:
        minio_client = Minio(
            config.minio.host + ':' + str(config.minio.port),
            access_key=config.minio.login,
            secret_key=config.minio.password,
            secure=False
        )
        return minio_client

    @provide(scope=Scope.APP)
    async def get_minio_config(self, config: Config) -> MinioConfig:
        return config.minio

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> interfaces.UUIDGenerator:
        return uuid4

    @provide(scope=Scope.REQUEST)
    async def get_async_session(self, async_sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AnyOf[AsyncSession, interfaces.DBSession]]:
        async with async_sessionmaker() as session:
            yield session
            
    user_repository = provide(UserRepository, scope=Scope.REQUEST, provides=AnyOf[interfaces.UserCreater, interfaces.UserUpdater, interfaces.UserGetter, interfaces.UserDeletter, interfaces.UserGetterByLoginPassword])
    video_repository = provide(VideoRepository, scope=Scope.REQUEST, provides=AnyOf[interfaces.UserVideoSearcher, interfaces.VideoCreater, interfaces.VideoGetter])
    heatmap_repository = provide(HeatMapRepository, scope=Scope.REQUEST, provides=AnyOf[interfaces.HeatMapCreater, interfaces.HeatMapGetter])

    create_user_validator = provide(validators.CreateUserValidator, scope=Scope.APP, provides=AnyOf[interfaces.CreateUserValidator])
    update_user_validator = provide(validators.UpdateUserValidator, scope=Scope.APP, provides=AnyOf[interfaces.UpdateUserValidator])
    search_user_videos_validator = provide(validators.SearchUserVideosValidator, scope=Scope.APP, provides=AnyOf[interfaces.SearchUserVideosValidator])
    create_video_validator = provide(validators.CreateVideoValidator, scope=Scope.APP, provides=AnyOf[interfaces.CreateVideoValidator])
    create_heat_map_validator = provide(validators.CreateHeatMapValidator, scope=Scope.APP, provides=AnyOf[interfaces.CreateHeatMapValidator])
    get_video_unload_link_validator = provide(validators.GetVideoUnloadLinkValidator, scope=Scope.APP, provides=AnyOf[interfaces.GetVideoUnloadLinkValidator])
    get_heat_map_unload_link_validator = provide(validators.GetHeatMapUnloadLinkValidator, scope=Scope.APP, provides=AnyOf[interfaces.GetHeatMapUnloadLinkValidator])
    generate_user_token_validator = provide(validators.GenerateUserTokenValidator, scope=Scope.APP, provides=AnyOf[interfaces.GenerateUserTokenValidator])

    create_user_authAdd = provide(auth.Auth, scope=Scope.REQUEST, provides=AnyOf[interfaces.AuthAdder])
    update_user_authCurrentUserGetter = provide(auth.Auth, scope=Scope.REQUEST, provides=AnyOf[interfaces.AuthCurrentUserGetter])

    file_storage = provide(file_storage.FileStorage, scope=Scope.REQUEST, provides=AnyOf[interfaces.GetFileUploadLink, interfaces.GetFileUnloadLink])

    create_user_interactor = provide(CreateUserInteractor, scope=Scope.REQUEST)
    update_user_interactor = provide(UpdateUserInteractor, scope=Scope.REQUEST)
    get_user_interactor = provide(GetUserInteractor, scope=Scope.REQUEST)
    delete_user_interactor = provide(DeleteUserInteractor, scope=Scope.REQUEST)
    search_user_video_interactor = provide(SearchUserVideosInteractor, scope=Scope.REQUEST)
    create_video_interactor = provide(CreateVideoInteractor, scope=Scope.REQUEST)
    create_heat_map_interactor = provide(CreateHeatMapInteractor, scope=Scope.REQUEST)
    get_video_unload_link_interactor = provide(GetVideoUnloadLinkInteractor, scope=Scope.REQUEST)
    get_heat_map_unload_link_interactor = provide(GetHeatMapUnloadLinkInteractor, scope=Scope.REQUEST)
    generate_user_token_interactor = provide(GenerateUserTokenInteractor, scope=Scope.REQUEST)