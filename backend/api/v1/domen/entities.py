from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class User:
    uuid: int
    login: str
    email: str
    password: str
    
@dataclass(slots=True)    
class Video:
    uuid: int
    name: str
    author: User
    length_seconds: int
    size: str
    uploaded_at: datetime.date
    
@dataclass(slots=True)
class HeatMap:
    uuid: int
    video: Video
    heat_map_data: dict
    



    