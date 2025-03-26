from abc import abstractmethod  
from typing import Protocol
from domen import entities
from uuid import UUID
from typing import NewType
import datetime
from application import dto

Token = NewType('Token', str)

class UserCreater(Protocol):
    @abstractmethod
    def create(self, user: entities.User) -> None:
        pass
    
class CreateUserValidator(Protocol):
    @abstractmethod
    def validate(self, user: dto.CreateUserInDTO) -> None:
        pass
    
class DBSession(Protocol):
    @abstractmethod
    def commit(self) -> None:
        pass

class UUIDGenerator(Protocol):
    def __call__(self) -> UUID:
        ...

class AuthAdder(Protocol):
    @abstractmethod
    async def add(self, user_id: str) -> Token:
        pass

class AuthCurrentUserGetter(Protocol):
    @abstractmethod
    async def get_current_user() -> str | None:
        pass

class UserUpdater(Protocol):
    @abstractmethod
    def update(self, user_id: str, fields: dict[str, str]) -> None:
        pass

class UpdateUserValidator(Protocol):
    @abstractmethod
    def validate(self, user: dto.UpdateUserInDTO) -> None:
        pass

class UserGetter(Protocol):
    @abstractmethod
    def get(self, user_id: str) -> entities.User:
        pass

class UserDeletter(Protocol):
    @abstractmethod
    def delete(self, user_id: str) -> None:
        pass

class UserVideoSearcher(Protocol):
    @abstractmethod
    def search(self, user_id: str, date: datetime.date | None, count: int, cursor: str | None) -> dict:
        pass

class SearchUserVideosValidator(Protocol):
    @abstractmethod
    def validate(self, count: int, date: datetime.date | None) -> None:
        pass

class VideoCreater(Protocol):
    @abstractmethod
    def create(self, video: dto.CreateVideoInDTO) -> None:
        pass

class VideoGetter(Protocol):
    @abstractmethod
    def get_by_author_and_name(self, author: str, name: str) -> entities.Video:
        pass

class CreateVideoValidator(Protocol):
    @abstractmethod
    def validate(self, video: dto.CreateVideoInDTO) -> None:
        pass

class GetFileUploadLink(Protocol):
    @abstractmethod
    def get_upload_link(self, file_name: str) -> str:
        pass

class GetFileUnloadLink(Protocol):
    @abstractmethod
    def get_unload_link(self, file_name: str) -> str:
        pass

class HeatMapCreater(Protocol):
    @abstractmethod
    def create(self, heat_map: entities.HeatMap) -> None:
        pass

class CreateHeatMapValidator(Protocol):
    @abstractmethod
    def validate(self, video_name: dto.CreateHeatMapInDTO) -> None:
        pass