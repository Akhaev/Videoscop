from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class CreateUserDTO:
    login: str
    name: str
    email: str
    password: str
    
@dataclass(slots=True)
class UpdateUserDto:
    login: str
    name: str
    email: str
    password: str
