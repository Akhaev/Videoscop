import re
import datetime
from .exceptions import ValidationError
from . import interfaces
from . import dto

def is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[\w.-]+@[\w.-]+\.\w+$", email))
    
def is_valid_login(login: str) -> bool:
    return 3 <= len(login) <= 50

def is_valid_password(password: str) -> bool:
    return len(password) >= 8

def is_valid_video_name(name: str) -> bool:
    return 3 <= len(name) <= 50

class CreateUserValidator(interfaces.CreateUserValidator):
    def validate(self, user: dto.CreateUserInDTO) -> None:
        errors = []

        if not is_valid_login(user.login):
            errors.append(ValidationError.add_error("login", "Login must be between 3 and 50 characters"))
        if not is_valid_email(user.email):
            errors.append(ValidationError.add_error("email", "Invalid email format"))
        if not is_valid_password(user.password):
            errors.append(ValidationError.add_error("password", "Password must be at least 8 characters long"))

        if errors:
            raise ValidationError(errors)

class UpdateUserValidator(interfaces.UpdateUserValidator):
    def validate(self, user: dto.UpdateUserInDTO) -> None:
        errors = []

        if user.login is not None and not is_valid_login(user.login):
            errors.append(ValidationError.add_error("login", "Login must be between 3 and 50 characters"))

        if user.email is not None and not is_valid_email(user.email):
            errors.append(ValidationError.add_error("email", "Invalid email format"))

        if user.password is not None and not is_valid_password(user.password):
            errors.append(ValidationError.add_error("password", "Password must be at least 8 characters long"))

        if not any(field is not None for field in [user.login, user.email, user.password]):
            errors.append(ValidationError.add_error("general", "At least one field must be provided"))

        if errors:
            raise ValidationError(errors)

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
    def validate(self, video: dto.CreateVideoInDTO) -> None:
        errors = []

        if not is_valid_video_name(video.name):
            errors.append(ValidationError.add_error("name", "Name must be between 3 and 50 characters"))

        if errors:
            raise ValidationError(errors)

class CreateHeatMapValidator(interfaces.CreateHeatMapValidator):
    def validate(self, video_name: str) -> None:
        errors = []

        if not is_valid_video_name(video_name):
            errors.append(ValidationError.add_error("video_name", "Name must be between 3 and 50 characters"))

        if errors:
            raise ValidationError(errors)

class GetVideoUnloadLinkValidator(interfaces.GetVideoUnloadLinkValidator):
    def validate(self, video_dto: dto.GetVideoUnloadLinkInDto) -> None:
        errors = []

        if not is_valid_video_name(video_dto.video_name):
            errors.append(ValidationError.add_error("video_name", "Name must be between 3 and 50 characters"))

        if errors:
            raise ValidationError(errors)

class GetHeatMapUnloadLinkValidator(interfaces.GetHeatMapUnloadLinkValidator):
    def validate(self, heatmap_dto: dto.GetHeatMapUnloadLinkInDto) -> None:
        errors = []

        if not is_valid_video_name(heatmap_dto.video_name):
            errors.append(ValidationError.add_error("video_name", "Name must be between 3 and 50 characters"))

        if errors:
            raise ValidationError(errors)

class GenerateUserTokenValidator(interfaces.GenerateUserTokenValidator):
    def validate(self, user_dto: dto.GenerateUserTokenInDTO) -> None:
        errors = []

        if user_dto.login is None and user_dto.email is None:
            errors.append(ValidationError.add_error("general", "Either login or email must be provided"))
        if user_dto.login is not None and not is_valid_login(user_dto.login):
            errors.append(ValidationError.add_error("login", "Login must be between 3 and 50 characters"))
        elif user_dto.email is not None and not is_valid_email(user_dto.email):
            errors.append(ValidationError.add_error("email", "Invalid email format"))
        if not is_valid_password(user_dto.password):
            errors.append(ValidationError.add_error("password", "Password must be at least 8 characters long"))

        if errors:
            raise ValidationError(errors)
