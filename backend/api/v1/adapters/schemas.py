from pydantic import BaseModel, Field
import datetime


class CreateUser(BaseModel):
    login: str = Field(title='Login of the user')
    email: str = Field(title='Email of the user')
    password: str = Field(title='Password of the user')

class UpdateUser(BaseModel):
    login: str | None = Field(title='Login of the user')
    email: str | None = Field(title='Email of the user')
    password: str | None = Field(title='Password of the user')
    current_password: str | None = Field(default=None, title='Current password of the user (required if updating email or password)')

class GetUser(BaseModel):
    login: str = Field(title='Login of the user')
    email: str = Field(title='Email of the user')

class Video(BaseModel):
    name: str = Field(title='Name of the video')
    length_seconds: int = Field(title='Length of the video')
    size: str = Field(title='Size of the video')
    uploaded_at: datetime.date = Field(title='Date of the video')

class SearchVideoIn(BaseModel):
    date: datetime.date | None = Field(title='Date of the video', default=None)
    count: int = Field(title='Count of the video')
    cursor: str | None = Field(title='Cursor of the video', default=None)

class SearchVideoOut(BaseModel):
    videos: list[Video] = Field(title='List of videos')
    cursor: str | None = Field(title='Cursor of the video')

class CreateVideoIn(BaseModel):
    name: str = Field(title='Name of the video')
    length_seconds: int = Field(title='Length of the video')
    size: int = Field(title='Size of the video')