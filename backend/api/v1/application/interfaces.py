from abc import abstractmethod  
from typing import Protocol
from domen import entities
from uuid import UUID
from typing import NewType


Token = NewType('Token', str)



class UserCreater(Protocol):
    @abstractmethod
    def create(self, user: entities.User ) -> None:
        pass
    
class CreateUserValidator(Protocol):

    @abstractmethod
    def validate(self, user: entities.User) -> None:
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
    async def get_current_user(self) -> str | None:
        pass

class UserUpdater(Protocol):
    @abstractmethod
    def update(self, user_id: str, fields: dict[str:str] ) -> None:
        pass
    
    
class UpdateUserValidator(Protocol):
    
    @abstractmethod
    def validate(self, fields: dict[str:str]) -> None:
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
    def search(self, user_id: str) -> list[entities.Video] | None:
        pass