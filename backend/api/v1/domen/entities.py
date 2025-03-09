from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class User:
    uuid: int
    login: str
    name: str
    email: str
    password: str
    
@dataclass(slots=True)    
class Video:
    uuid: int
    name: str
    author: User
    length_seconds: int
    format_: str
    size: str
    
@dataclass(slots=True)
class HeatMap:
    uuid: int
    video: Video
    heat_map_data: dict
    
@dataclass(slots=True)
class Session:
    uuid: int
    user: User
    video: Video
    start_time: datetime.date
    end_time: datetime.date 
    

@dataclass(slots=True)
class UserToken:
    uuid: int
    user: User
    token: str
    