from abc import abstractmethod  
from typing import Protocol
from domen import entities
from uuid import UUID
    
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
    
