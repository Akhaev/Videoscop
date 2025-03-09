
response_409 = {
    "description": "Conflict: the fields already exists",
    "content": {
        "application/json": {
            "example": {
                "message": "conflict field/fields",
                "problem_fields": {
                    "email": "exists field",
                }
            }
        }
    }
}


response_201 = {
            "description": "Successful authentication, returns the access token",
            "content": {
                "application/json": {
                    "example": {
                        "token": "user token for authentication",
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


response_401_expired = {
    "description": "Unauthorized: The token has expired.",
    "content": {
        "application/json": {
            "example": {
                "message": "Token has expired",
            }
        }
    }
}

response_401_invalid = {
    "description": "Unauthorized: The token is invalid.",
    "content": {
        "application/json": {
            "example": {
                "message": "Invalid token",
            }
        }
    }
}

response_401_missing = {
    "description": "Unauthorized: The token is missing or has an invalid format.",
    "content": {
        "application/json": {
            "example": {
                "message": "Authorization token is missing or improperly formatted",
            }
        }
    }
}
