from dataclasses import dataclass, field
from datetime import date
from typing import get_type_hints

@dataclass(slots=True)
class User:
    uuid: str
    login: str
    email: str
    password: str

    def __post_init__(self):
        for field_name, field_type in get_type_hints(self.__class__).items():
            if not isinstance(getattr(self, field_name), field_type):
                raise TypeError(f"Field '{field_name}' must be of type {field_type}")

@dataclass(slots=True)    
class Video:
    uuid: str
    name: str
    author_uuid: str
    length_seconds: int
    size: int
    uploaded_at: date

    def __post_init__(self):
        for field_name, field_type in get_type_hints(self.__class__).items():
            if not isinstance(getattr(self, field_name), field_type):
                raise TypeError(f"Field '{field_name}' must be of type {field_type}")

@dataclass(slots=True)
class HeatMap:
    uuid: str
    video_uuid: str

    def __post_init__(self):
        for field_name, field_type in get_type_hints(self.__class__).items():
            if not isinstance(getattr(self, field_name), field_type):
                raise TypeError(f"Field '{field_name}' must be of type {field_type}")





