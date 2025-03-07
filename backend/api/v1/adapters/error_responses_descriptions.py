
response_409 = {
    "description": "Conflict: the resource already exists in the system.",
    "content": {
        "application/json": {
            "example": {
                "message": "incorrect field/fields",
                "problem_fields": {
                    "email": "invalid email format",
                    "password": "password must be at least 8 characters long"
                }
            }
        }
    }
}





response_422 = {
    "description": "Validation error: some fields contain incorrect data.",
    "content": {
        "application/json": {
            "example": {
                "message": "incorrect field/fields",
                "problem_fields": {
                    "email": "invalid email format",
                    "password": "password must be at least 8 characters long"
                }
            }
        }
    }
}