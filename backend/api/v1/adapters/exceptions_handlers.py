from fastapi import Request, status
from fastapi.responses import JSONResponse
from asyncpg.exceptions import UniqueViolationError
import json
import jwt
from application.exceptions import UnAuthorizedError, ValidationError
from infrastructure.db.exceptions import RecordDontExistsError

# Этот хендлер срабатывает, когда возникает ошибка валидации данных.
async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    problem_fields = {error["loc"][-1]: error["msg"] for error in exc.errors()}
    
    error_message = {
        "message": "conflict field/fields",
        "problem_fields": problem_fields
    }
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=json.dumps(error_message)
    )

# Этот хендлер срабатывает, когда возникает ошибка уникальности данных в базе данных.
async def integrity_error_handler(request: Request, exc: UniqueViolationError) -> JSONResponse:
    problem_fields = {field: "already exists" for field in exc.args[0]}
    
    error_message = {
        "message": "Conflict field/fields",
        "problem_fields": problem_fields
    }
    
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=json.dumps(error_message)
    )

# Этот хендлер срабатывает, когда токен истек.
async def expired_token_handler(request: Request, exc: jwt.ExpiredSignatureError):
    return JSONResponse(
        status_code=401,
        content={"message": "Token has expired"},
    )

# Этот хендлер срабатывает, когда токен недействителен.
async def invalid_token_handler(request: Request, exc: jwt.InvalidTokenError):
    return JSONResponse(
        status_code=401,
        content={"message": "Invalid token"},
    )

# Этот хендлер срабатывает, когда токен отсутствует или имеет неправильный формат.
async def unauthorized_handler(request: Request, exc: UnAuthorizedError):
    return JSONResponse(
        status_code=401,
        content={"message": "Authorization token is missing or improperly formatted"},
    )

# Этот хендлер срабатывает, когда возникает ошибка значения.
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)},
    )

# Этот хендлер срабатывает, когда запись не найдена в базе данных.
async def record_not_found_handler(request: Request, exc: RecordDontExistsError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)},
    )

all_handlers = { 
    UniqueViolationError: integrity_error_handler,
    jwt.ExpiredSignatureError: expired_token_handler,
    jwt.InvalidTokenError: invalid_token_handler,
    UnAuthorizedError: unauthorized_handler,
    ValidationError: validation_exception_handler,
    ValueError: value_error_handler,
    RecordDontExistsError: record_not_found_handler
}