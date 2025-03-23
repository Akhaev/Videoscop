import re
import datetime
from .exceptions import ValidationError
from . import interfaces
from . import dto

class CreateUserValidator(interfaces.CreateUserValidator):
    def validate(self, user: dto.CreateUserDTO) -> None:
        errors = []

        if not (3 <= len(user.login) <= 50):
            errors.append(ValidationError.add_error("login", "Login must be between 3 and 50 characters"))
        if not self.is_valid_email(user.email):
            errors.append(ValidationError.add_error("email", "Invalid email format"))
        if len(user.password) < 8:
            errors.append(ValidationError.add_error("password", "Password must be at least 8 characters long"))

        if errors:
            raise ValidationError(errors)

    @staticmethod
    def is_valid_email(email: str) -> bool:
        return bool(re.match(r"^[\w.-]+@[\w.-]+\.\w+$", email))

class UpdateUserValidator(interfaces.UpdateUserValidator):
    def validate(self, user: dto.UpdateUserDto) -> None:
        errors = []

        if user.login is not None:
            if not (3 <= len(user.login) <= 50):
                errors.append(ValidationError.add_error("login", "Login must be between 3 and 50 characters"))

        if user.email is not None:
            if not self.is_valid_email(user.email):
                errors.append(ValidationError.add_error("email", "Invalid email format"))

        if user.password is not None:
            if len(user.password) < 8:
                errors.append(ValidationError.add_error("password", "Password must be at least 8 characters long"))

        if not any(field is not None for field in [user.login, user.email, user.password]):
            errors.append(ValidationError.add_error("general", "At least one field must be provided"))

        if errors:
            raise ValidationError(errors)

    @staticmethod
    def is_valid_email(email: str) -> bool:
        return bool(re.match(r"^[\w.-]+@[\w.-]+\.\w+$", email))

class SearchUserVideosValidator(interfaces.SearchUserVideosValidator):
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

class CreateVideoValidator(interfaces.CreateVideoValidator):
    def validate(self, video: dto.CreateVideoDTO) -> None:
        errors = []

        if not (3 <= len(video.name) <= 50):
            errors.append(ValidationError.add_error("name", "Name must be between 3 and 50 characters"))
        if not (1 <= video.length_seconds <= 3600):
            errors.append(ValidationError.add_error("length_seconds", "Length must be between 1 and 3600 seconds"))
        if not isinstance(video.size, int) or not (1 <= video.size <= 1000):  # Проверка на int
            errors.append(ValidationError.add_error("size", "Size must be an integer between 1 and 1000 MB"))

        if errors:
            raise ValidationError(errors)