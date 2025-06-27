from dataclasses import dataclass
from datetime import date
from typing import Optional, List

@dataclass(slots=True)
class CreateUserInDTO:
    login: str
    email: str
    password: str

@dataclass(slots=True)
class CreateUserOutDTO:
    token: str

@dataclass(slots=True)
class UpdateUserInDTO:
    login: Optional[str]
    email: Optional[str]
    password: Optional[str]
    current_password: Optional[str]

@dataclass(slots=True)
class UpdateUserOutDTO:
    message: str

@dataclass(slots=True)
class GetUserOutDTO:
    login: str
    email: str

@dataclass(slots=True)
class DeleteUserOutDTO:
    message: str

@dataclass(slots=True)
class SearchUserVideosInDTO:
    date: Optional[date]
    count: int
    cursor: Optional[str]

@dataclass(slots=True)
class SearchUserVideosOutDTO:
    videos: List[dict]
    cursor: Optional[str]

@dataclass(slots=True)
class CreateVideoInDTO:
    name: str
    length_seconds: int
    size: int

@dataclass(slots=True)
class CreateVideoOutDTO:
    upload_link: str

@dataclass(slots=True)
class CreateHeatMapInDTO:
    video_name: str

@dataclass(slots=True)
class CreateHeatMapOutDTO:
    upload_link: str

@dataclass(slots=True)
class GetVideoUnloadLinkInDto:
    video_name: str

@dataclass(slots=True)
class GetVideoUnloadLinkOutDTO:
    unload_link: str

@dataclass(slots=True)
class GetHeatMapUnloadLinkInDto:
    video_name: str

@dataclass(slots=True)
class GetHeatMapUnloadLinkOutDTO:
    unload_link: str

@dataclass(slots=True)
class GenerateUserTokenInDTO:
    password: str
    login: str | None = None
    email: str | None = None
@dataclass(slots=True)
class GenerateUserTokenOutDTO:
    token: str