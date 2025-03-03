from dishka import Provider, provide, Scope, from_context, AnyOf
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from config import Config
from infrastructure.database import new_session_maker
from typing import AsyncIterable
from application.interfaces import DBSession

class FastApiApp(Provider):
    
    config = from_context(provides=Config, scope=Scope.APP)
    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)
    
    
    @provide(scope=Scope.REQUEST)
    async def get_async_session(self, async_sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AnyOf[AsyncSession,DBSession]]:
        async with async_sessionmaker() as session:
            yield session