from abc import abstractmethod  
from typing import Protocol
from domen import entities

    
class UserCreater(Protocol):
    @abstractmethod
    def create_user(self, user: entities.User ) -> None:
        pass
    
class DBSession(Protocol):
    
    @abstractmethod
    def commit(self) -> None:
        pass