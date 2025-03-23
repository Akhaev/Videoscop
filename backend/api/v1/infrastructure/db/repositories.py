from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, text
from application import interfaces
from domen import entities
from . import models
from asyncpg import UniqueViolationError
import hashlib
from sqlalchemy import Column
from typing import Any, Tuple
from . import exceptions
import datetime
import time

def Sha512Hash(text: str) -> str:
    hashed_password = hashlib.sha512(text.encode('utf-8')).hexdigest()
    return hashed_password

class UserRepository(interfaces.UserCreater, interfaces.UserUpdater):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: entities.User) -> None:
        user = models.User(uuid=user.uuid, login=user.login, email=user.email, password=Sha512Hash(user.password))
        self.session.add(user)

    async def update(self, user_uuid: str, update_fields: dict[str:str]) -> None:
        user = await self.get_by_uuid(user_uuid)
        query = update(models.User).where(models.User.uuid == user_uuid).values(update_fields)
        await self.session.execute(query)

    async def exists_by(self, column: Column, value: str) -> bool:
        query = select(models.User).where(column == value).exists()
        exists = await self.session.scalar(select(query))
        return exists

    async def exists_by_columns(self, columns: list[Column], values: list[Any]) -> Tuple[bool, list[str]]:
        from sqlalchemy import or_
        
        conditions = [column == value for column, value in zip(columns, values)]
        query = select(models.User).where(or_(*conditions)).exists()
        exists = await self.session.scalar(select(query))
        
        if not exists:
            return False, []
        
        existing_fields = [
            column.name for column, value in zip(columns, values)
            if await self.exists_by(column, value)
        ]
        return True, existing_fields

    async def get_by_uuid(self, user_uuid: str) -> models.User:  # Изменено с get_by_id на get_by_uuid
        user = await self.session.get(models.User, user_uuid)
        if user is None:
            raise exceptions.RecordDontExistsError('User not found')
        return user

    async def get(self, user_uuid: str) -> entities.User:
        user = await self.get_by_uuid(user_uuid)  # Изменено с get_by_id на get_by_uuid
        return entities.User(uuid=user.uuid, login=user.login, email=user.email, password=user.password)

    async def delete(self, user_uuid: str) -> None:
        user = await self.get_by_uuid(user_uuid)  # Изменено с get_by_id на get_by_uuid
        await self.session.delete(user)
    
class VideoRepository(interfaces.UserVideoSearcher):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def create(self, video: entities.Video) -> None:
        video = models.Video(
            uuid=video.uuid, 
            name=video.name, 
            author_uuid=video.author, 
            length_seconds=video.length_seconds, 
            size=video.size,
            uploaded_at=video.uploaded_at
        )
        
        self.session.add(video)

    async def search(self, user_uuid: str, date: datetime.date | None, count: int, cursor: str | None) -> dict['videos': list[entities.Video], 'cursor': str] | None:
        videos = []
        
        user_exists = await UserRepository(self.session).exists_by(models.User.uuid, user_uuid)
        
        if not user_exists:
            raise exceptions.RecordDontExistsError('User not found')

        if cursor is None:
            current_time = int(time.time() * 1000)
            cursor = hashlib.sha512(f'user_id_{user_uuid}_{current_time}'.encode('utf-8')).hexdigest()

            declare_query = text(f"""
                DECLARE "{cursor}" CURSOR WITH HOLD FOR 
                SELECT * FROM videos 
                WHERE author_uuid = :user_uuid AND uploaded_at = :date
                ORDER BY name
            """)

            await self.session.execute(declare_query, {"user_uuid": user_uuid, "date": date})

        fetch_query = text(f"""
            FETCH FORWARD {int(count)} FROM "{cursor}"
        """)

        result = await self.session.execute(fetch_query)
        
        rows = result.fetchall()
        
        if not rows:
            await self.session.execute(text(f'CLOSE "{cursor}"'))
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