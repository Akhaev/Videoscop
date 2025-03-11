from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from application import interfaces
from domen import entities
from . import models
from asyncpg import UniqueViolationError
import hashlib
from sqlalchemy import Column
from typing import Any
from . import exceptions

def Sha512Hash(password: str) -> str:
    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    return hashed_password

class UserRepository(interfaces.UserCreater, interfaces.UserUpdater):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def _exists_by(self, column: Column, value: str):
        query = select(models.User).where(column == value).exists()
        exists = await self.session.scalar(select(query))
        if exists:
            raise UniqueViolationError([column.name])
    
    async def _exists_by_columns(self, columns: list[Column], values: list[Any]) -> None:
        exists_fields = []
        for column, value in zip(columns, values):
            query = select(models.User).where(column == value).exists()
            exists = await self.session.scalar(select(query))
            if exists:
                exists_fields.append(column.name)
        if exists:                
            raise UniqueViolationError(exists_fields)
        
    async def get_by_id(self, user_id: str) -> entities.User | None:
        user = await self.session.get(models.User, user_id)
        return user
        
    
    async def create(self, user: entities.User) -> None:

        
        await self._exists_by_columns([models.User.login, models.User.email], [user.login, user.email])
        
        user = models.User(uuid=user.uuid, login=user.login, name=user.name, email=user.email, password=Sha512Hash(user.password))

        
        self.session.add(user)
        
    

    async def update (self, user_id: str, update_fields: dict[str:str]) -> None:
        user = await self.session.get(models.User, user_id)
        if user is None:
            raise exceptions.RecordDontExistsError('User not found')
        user.update(update_fields)
            