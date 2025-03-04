from pydantic import BaseModel, Field

class CreateUser(BaseModel):
    login: str = Field(title='Login of the user')
    name: str = Field(title='Name of the user')
    email: str = Field(title='Email of the user')
    password: str = Field(title='Password of the user')
