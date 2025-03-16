from dataclasses import dataclass
import re
from .exceptions import ValidationError
from .interfaces import CreateUserValidator, UpdateUserValidator
from . import dto
@dataclass
class CreateUser:
    login: str
    email: str
    password: str

    def __post_init__(self):
        self.validate()

    def validate(self):
        errors = []

        if not (3 <= len(self.login) <= 50):
            errors.append(ValidationError.add_error("login", "Login must be between 3 and 50 characters"))
        if not self.is_valid_email(self.email):
            errors.append(ValidationError.add_error("email", "Invalid email format"))
        if len(self.password) < 8:
            errors.append(ValidationError.add_error("password", "Password must be at least 8 characters long"))

        if errors:
            raise ValidationError(errors)

    @staticmethod
    def is_valid_email(email: str) -> bool:
        return bool(re.match(r"^[\w.-]+@[\w.-]+\.\w+$", email))

class CreateUserValidator(UpdateUserValidator):
    def validate(self, user: dto.CreateUserDTO):
        try:
            CreateUser(
                login=user.login,
                email=user.email,
                password=user.password
            )
        except ValidationError as e:
            raise e
        
        
@dataclass
class UpdateUser:
    login: str | None
    email: str | None
    password: str | None

    def __post_init__(self):
        self.validate()

    def validate(self):
        errors = []

        if self.login is not None:
            if not (3 <= len(self.login) <= 50):
                errors.append(ValidationError.add_error("login", "Login must be between 3 and 50 characters"))

        if self.email is not None:
            if not self.is_valid_email(self.email):
                errors.append(ValidationError.add_error("email", "Invalid email format"))

        if self.password is not None:
            if len(self.password) < 8:
                errors.append(ValidationError.add_error("password", "Password must be at least 8 characters long"))

        if not any(field is not None for field in [self.login, self.email, self.password]):
            errors.append(ValidationError.add_error("general", "At least one field must be provided"))

        if errors:
            raise ValidationError(errors)

    @staticmethod
    def is_valid_email(email: str) -> bool:
        return bool(re.match(r"^[\w.-]+@[\w.-]+\.\w+$", email))


class UpdateUserValidator(CreateUserValidator):
    def validate(self, user: dto.UpdateUserDto):
        try:
            UpdateUser(
                login=user.login,
                email=user.email,
                password=user.password
            )
        except ValidationError as e:
            raise e