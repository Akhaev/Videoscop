from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from asyncpg.exceptions import UniqueViolationError
from fastapi import status
import json
import jwt
from infrastructure.auth.exceptions import UnAuthorizedError
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


async def expired_token_handler(request: Request, exc: jwt.ExpiredSignatureError):
    return JSONResponse(
        status_code=401,
        content={"message": "Token has expired"},
    )



async def invalid_token_handler(request: Request, exc: jwt.InvalidTokenError):
    return JSONResponse(
        status_code=401,
        content={"message": "Invalid token"},
    )


async def unauthorized_handler(request: Request, exc: UnAuthorizedError):
    return JSONResponse(
        status_code=401,
        content={"message": "Authorization token is missing or improperly formatted"},
    )

all_handlers = {
    ValidationError: validation_exception_handler,  
    UniqueViolationError: integrity_error_handler,
    jwt.ExpiredSignatureError: expired_token_handler,
    jwt.InvalidTokenError: invalid_token_handler,
    UnAuthorizedError: unauthorized_handler,
    
}