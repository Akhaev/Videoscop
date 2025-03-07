from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from asyncpg.exceptions import UniqueViolationError
from fastapi import status
import json
async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    problem_fields = {error["loc"][-1]: error["msg"] for error in exc.errors()}
    
    error_message = {
        "message": "incorrect field/fields",
        "problem_fields": problem_fields
    }
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=json.dumps(error_message)
    )

async def integrity_error_handler(request: Request, exc: UniqueViolationError) -> JSONResponse:
    problem_fields = {field: "already exists" for field in exc.args[0]}
    
    error_message = {
        "message": "incorrect field/fields",
        "problem_fields": problem_fields
    }
    
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=json.dumps(error_message)
    )
        
all_handlers = {
    ValidationError: validation_exception_handler,  
    UniqueViolationError: integrity_error_handler,
    
}