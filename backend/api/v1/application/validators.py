from dataclasses import dataclass
import re
import datetime
from .exceptions import ValidationError
from . import interfaces
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

class CreateUserValidator(interfaces.CreateUserValidator):
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


class UpdateUserValidator(interfaces.UpdateUserValidator):
    def validate(self, user: dto.UpdateUserDto):
        try:
            UpdateUser(
                login=user.login,
                email=user.email,
                password=user.password
            )
        except ValidationError as e:
            raise e

class UserSearchVideosValidator(interfaces.UserSearchVideosValidator):
    def validate(self, count: int, date: datetime.date | None) -> None:
        errors = []

        if not isinstance(count, int) or count <= 0:
            errors.append(ValidationError.add_error("count", "Count must be a positive integer"))
        if count > 15:
            errors.append(ValidationError.add_error("count", "Count cannot be greater than 15"))

        if date is not None:
            if not isinstance(date, datetime.date):
                errors.append(ValidationError.add_error("date", "Invalid date format"))
            if date < datetime.date(2025, 3, 1):
                errors.append(ValidationError.add_error("date", "Date cannot be earlier than March 1, 2025"))
            if date > datetime.date.today():
                errors.append(ValidationError.add_error("date", "Date cannot be in the future"))

        if errors:
            raise ValidationError(errors)