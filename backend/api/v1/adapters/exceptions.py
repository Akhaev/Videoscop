from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from asyncpg.exceptions import UniqueViolationError

async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"message": f"{exc.errors()}"},
    )
    
async def integrity_error_handler(request: Request, exc: UniqueViolationError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.msg}
    )
        
all_exceptions = {
    ValidationError: validation_exception_handler,  
    UniqueViolationError: integrity_error_handler,
    
}