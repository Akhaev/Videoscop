from pydantic import BaseModel, EmailStr, Field
from application.interfaces import CreateUserValidator

class CreateUser(BaseModel):
    login: str = Field(min_length=3, max_length=50)
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)
    
class UserValidator(CreateUserValidator):


    def validate(self, user):
            CreateUser(
            login=user.login,
            name=user.name,
            email=user.email,
            password=user.password
        )
