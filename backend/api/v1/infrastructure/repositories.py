from sqlalchemy.ext.asyncio import AsyncSession
from application import interfaces
from domen import entities
from . import models
import hashlib

def Sha512Hash(password: str) -> str:
    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    return hashed_password

class UserRepository(interfaces.UserCreater):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def create(self, user: entities.User) -> None:
        user = models.User(uuid=user.uuid, login=user.login, name=user.name, email=user.email, password=Sha512Hash(user.password))
        self.session.add(user)
        
    

