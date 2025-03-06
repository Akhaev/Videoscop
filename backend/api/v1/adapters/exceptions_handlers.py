from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from asyncpg.exceptions import UniqueViolationError
from fastapi import status
import json
async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": f"{exc.errors()}"},
    )
    
async def integrity_error_handler(request: Request, exc: UniqueViolationError) -> JSONResponse:
    exists_fields = exc.args[0]
    
    error_message = {
            "message": "fields already exists",
            "problem_fields": exists_fields
        }
    
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=json.dumps(error_message))
        
all_handlers = {
    ValidationError: validation_exception_handler,  
    UniqueViolationError: integrity_error_handler,
    
}