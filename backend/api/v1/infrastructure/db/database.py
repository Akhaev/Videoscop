from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config import PostgresConfig
from . import models
from sqlalchemy.pool import NullPool

async def new_session_maker(psql_config: PostgresConfig) -> async_sessionmaker[AsyncSession]:
    database_uri = "postgresql+asyncpg://{login}:{password}@{host}:{port}/{database}".format(
        login=psql_config.login,
        password=psql_config.password,
        host=psql_config.host,
        port=psql_config.port,
        database=psql_config.database,
    )

    engine = create_async_engine(
        database_uri,

        poolclass=NullPool
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
    
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    
    return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)