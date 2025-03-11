from dataclasses import dataclass
import re
from .exceptions import ValidationError
from .interfaces import CreateUserValidator, UpdateUserValidator
from . import dto
@dataclass
class CreateUser:
    login: str
    name: str
    email: str
    password: str

    def __post_init__(self):
        self.validate()

    def validate(self):
        errors = []

        if not (3 <= len(self.login) <= 50):
            errors.append(ValidationError.add_error("login", "Login must be between 3 and 50 characters"))
        if not (1 <= len(self.name) <= 100):
            errors.append(ValidationError.add_error("name", "Name must be between 1 and 100 characters"))
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
                name=user.name,
                email=user.email,
                password=user.password
            )
        except ValidationError as e:
            raise e
        
        
@dataclass
class UpdateUser:
    login: str | None
    name: str | None
    email: str | None
    password: str | None

    def __post_init__(self):
        self.validate()

    def validate(self):
        errors = []

        # Check if any of the fields are not None, they must meet the validation rules.
        if self.login is not None:
            if not (3 <= len(self.login) <= 50):
                errors.append(ValidationError.add_error("login", "Login must be between 3 and 50 characters"))

        if self.name is not None:
            if not (1 <= len(self.name) <= 100):
                errors.append(ValidationError.add_error("name", "Name must be between 1 and 100 characters"))

        if self.email is not None:
            if not self.is_valid_email(self.email):
                errors.append(ValidationError.add_error("email", "Invalid email format"))

        if self.password is not None:
            if len(self.password) < 8:
                errors.append(ValidationError.add_error("password", "Password must be at least 8 characters long"))

        # Ensure that at least one field is not None
        if not any(field is not None for field in [self.login, self.name, self.email, self.password]):
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
                name=user.name,
                email=user.email,
                password=user.password
            )
        except ValidationError as e:
            raise e