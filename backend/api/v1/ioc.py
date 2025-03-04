from dishka import Provider, provide, Scope, from_context, AnyOf
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from config import Config
from infrastructure.database import new_session_maker
from typing import AsyncIterable
from application import interfaces
from infrastructure.repositories import UserRepository
from application.interactors import CreateUserInteractor
from uuid import uuid4
from infrastructure import validators


class FastApiApp(Provider):
    
    config = from_context(provides=Config, scope=Scope.APP)
    @provide(scope=Scope.APP)
    async def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        async_sessionmaker = await new_session_maker(config.postgres)
        return async_sessionmaker
    
    @provide(scope=Scope.REQUEST)
    async def get_async_session(self, async_sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AnyOf[AsyncSession,interfaces.DBSession]]:
        async with async_sessionmaker() as session:
            yield session
            
    user_repository = provide(UserRepository, scope=Scope.REQUEST, provides=AnyOf[interfaces.UserCreater])
    
    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> interfaces.UUIDGenerator:
        return uuid4
    
    create_user_validator = provide(validators.UserValidator, scope=Scope.APP, provides=AnyOf[interfaces.CreateUserValidator])
    
    create_user_interactor = provide(CreateUserInteractor, scope=Scope.REQUEST)
    
    