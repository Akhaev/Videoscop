from pydantic import BaseModel, Field
import datetime


class CreateUserIn(BaseModel):
    login: str = Field(
        title="Login of the user",
        description="The login must be a string between 3 and 50 characters.",
        min_length=3,
        max_length=50
    )
    email: str = Field(
        title="Email of the user",
        description="The email must be a valid email format.",
        pattern=r"^[\w.-]+@[\w.-]+\.\w+$"
    )
    password: str = Field(
        title="Password of the user",
        description="The password must be at least 8 characters long.",
        min_length=8
    )


class CreateUserOut(BaseModel):
    token: str = Field(
        title="Authentication token",
        description="A token used for authenticating the user."
    )


class UpdateUserIn(BaseModel):
    login: str | None = Field(
        title="Login of the user",
        description="The login must be a string between 3 and 50 characters. Optional.",
        min_length=3,
        max_length=50
    )
    email: str | None = Field(
        title="Email of the user",
        description="The email must be a valid email format. Optional.",
        pattern=r"^[\w.-]+@[\w.-]+\.\w+$"
    )
    password: str | None = Field(
        title="Password of the user",
        description="The password must be at least 8 characters long. Optional.",
        min_length=8
    )
    current_password: str | None = Field(
        default=None,
        title="Current password of the user",
        description="The current password is required if updating the email or password.",
        min_length=8
    )


class UpdateUserOut(BaseModel):
    message: str = Field(
        title="Update status message",
        description="A message indicating the result of the update operation."
    )


class GetUserOut(BaseModel):
    login: str = Field(
        title="Login of the user",
        description="The login of the user."
    )
    email: str = Field(
        title="Email of the user",
        description="The email of the user."
    )


class DeleteUserOut(BaseModel):
    message: str = Field(
        title="Deletion status message",
        description="A message indicating the result of the deletion operation."
    )


class CreateVideoIn(BaseModel):
    name: str = Field(
        title="Name of the video",
        description="The name must be a string between 3 and 50 characters.",
        min_length=3,
        max_length=50
    )
    length_seconds: int = Field(
        title="Length of the video",
        description="The length of the video in seconds. Must be between 1 and 3600.",
        ge=1,
        le=3600
    )
    size: int = Field(
        title="Size of the video",
        description="The size of the video in MB. Must be between 1 and 1000.",
        ge=1,
        le=1000
    )


class CreateVideoOut(BaseModel):
    upload_link: str = Field(
        title="Upload link",
        description="A link to upload the video."
    )


class SearchVideoIn(BaseModel):
    date: datetime.date | None = Field(
        title="Date of the video",
        description="The date when the video was uploaded. Optional.",
        default=None
    )
    count: int = Field(
        title="Number of videos to fetch",
        description="The number of videos to fetch. Must be between 1 and 15.",
        gt=0,
        le=15
    )
    cursor: str | None = Field(
        title="Pagination cursor",
        description="A cursor for pagination. Optional.",
        default=None
    )


class Video(BaseModel):
    name: str = Field(
        title="Name of the video",
        description="The name of the video."
    )
    length_seconds: int = Field(
        title="Length of the video",
        description="The length of the video in seconds."
    )
    size: int = Field(
        title="Size of the video",
        description="The size of the video in MB."
    )
    uploaded_at: datetime.date = Field(
        title="Upload date",
        description="The date when the video was uploaded."
    )


class SearchVideoOut(BaseModel):
    videos: list[Video] = Field(
        title="List of videos",
        description="A list of videos matching the search criteria."
    )
    cursor: str | None = Field(
        title="Pagination cursor",
        description="A cursor for fetching the next page of results. Optional."
    )


class CreateHeatMapIn(BaseModel):
    video_name: str = Field(
        title="Name of the video",
        description="The name of the video for which the heatmap is being created. Must be between 3 and 50 characters.",
        min_length=3,
        max_length=50
    )


class CreateHeatMapOut(BaseModel):
    upload_link: str = Field(
        title="Upload link for the heatmap",
        description="A link to upload the heatmap."
    )