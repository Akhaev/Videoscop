from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, text
from application import interfaces
from domen import entities
from . import models
from asyncpg import UniqueViolationError
import hashlib
from sqlalchemy import Column
from typing import Any
from . import exceptions
import datetime
import time

def Sha512Hash(text: str) -> str:
    hashed_password = hashlib.sha512(text.encode('utf-8')).hexdigest()
    return hashed_password

class UserRepository(interfaces.UserCreater, interfaces.UserUpdater):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def _exists_by(self, column: Column, value: str) -> None:
        query = select(models.User).where(column == value).exists()
        exists = await self.session.scalar(select(query))
        if exists:
            raise UniqueViolationError([column.name])
    
    async def _exists_by_columns(self, columns: list[Column], values: list[Any]) -> None:
        from sqlalchemy import or_
        
        conditions = [column == value for column, value in zip(columns, values)]
        query = select(models.User).where(or_(*conditions)).exists()
        exists = await self.session.scalar(select(query))
        if exists:
            exists_fields = [column.name for column, value in zip(columns, values) if await self._exists_by(column, value)]
            raise UniqueViolationError(exists_fields)
        
    async def get_by_id(self, user_id: str) -> models.User:
        user = await self.session.get(models.User, user_id)
        if user is None:
            raise exceptions.RecordDontExistsError('User not found')
        return user
        
    
    async def create(self, user: entities.User) -> None:

        
        await self._exists_by_columns([models.User.login, models.User.email], [user.login, user.email])
        
        user = models.User(uuid=user.uuid, login=user.login, email=user.email, password=Sha512Hash(user.password))

        
        self.session.add(user)

    async def update(self, user_id: str, update_fields: dict[str:str]) -> None:
        user = await self.get_by_id(user_id)
        query = update(models.User).where(models.User.uuid == user_id).values(update_fields)
        await self.session.execute(query)
    
    async def get(self, user_id: str) -> entities.User:
        user = await self.get_by_id(user_id)
        return entities.User(uuid=user.uuid, login=user.login, email=user.email, password=user.password)
    
    async def delete(self, user_id: str) -> None:
        user = await self.get_by_id(user_id)
        await self.session.delete(user)
    
class VideoRepository(interfaces.UserVideoSearcher):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def create(self, video: entities.Video) -> None:
        video = models.Video(uuid=video.uuid, name=video.name, author=video.author, 
                             length_seconds=video.length_seconds, size=video.size)
        self.session.add(video)

    async def search(self, user_id: str, date: datetime.date | None, count: int, cursor: str | None) -> dict['videos': list[entities.Video], 'cursor': str] | None:
        videos = []
        

        if cursor is None:
            current_time = int(time.time() * 1000)
            cursor = hashlib.sha512(f'user_id_{user_id}_{current_time}'.encode('utf-8')).hexdigest()

            declare_query = text("""
                DECLARE :cursor CURSOR WITH HOLD FOR 
                SELECT * FROM videos 
                WHERE author_uuid = :user_id AND uploaded_at = :date
                ORDER BY name
            """)

            await self.session.execute(declare_query, {"cursor": cursor, "user_id": user_id, "date": date})

        fetch_query = text("""
            FETCH :count FROM :cursor
        """)

        result = await self.session.execute(fetch_query, {"cursor": cursor, "count": count})
        
        rows = result.fetchall()
        
        if not rows:
            await self.session.execute(text("CLOSE :cursor"), {"cursor": cursor})
            return None
        
        videos = [
            entities.Video(
                uuid=video.uuid, 
                name=video.name, 
                author=video.author, 
                length_seconds=video.length_seconds, 
                size=video.size,
                uploaded_at=video.uploaded_at
            ) 
            for video in rows
        ]
        

        return {'videos': videos, 'cursor': cursor}