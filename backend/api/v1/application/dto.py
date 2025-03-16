from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class CreateUserDTO:
    login: str
    email: str
    password: str
    
@dataclass(slots=True)
class UpdateUserDto:
    login: str | None
    email: str | None
    password: str | None
    current_password: str | None = None

