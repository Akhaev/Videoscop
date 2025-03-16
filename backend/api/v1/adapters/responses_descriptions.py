
common_responses = {
        401: {
        "description": "Unauthorized: Various authentication errors.",
        "content": {
            "application/json": {
                "examples": {
                    "Token Expired": {
                        "value": {
                            "message": "Token has expired",
                        }
                    },
                    "Invalid Token": {
                        "value": {
                            "message": "Invalid token",
                        }
                    },
                    "Missing or Malformed Token": {
                        "value": {
                            "message": "Authorization token is missing or improperly formatted",
                        }
                    }
                }
            }
        }
    },
    
    
}

user_responses = {
    409: {
        "description": "Conflict: the user with this fields already exist.",
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
    },
    422: {
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
    },
    400: {
        "description": "Bad Request: The request could not be understood or was missing required parameters.",
        "content": {
            "application/json": {
                "example": {
                    "message": "requires an up-to-date password to update password or email",
                }
            }
        }
    },
    404:{
    "description": "Not Found: The authenticated or requested user was not found.",
    "content": {
        "application/json": {
            "example": {
                "message": "User not found",
            }
        }
    }
},
    201: {
        "description": "Successful authentication, returns the access token.",
        "content": {
            "application/json": {
                "example": {
                    "token": "user token for authentication",
                }
            }
        }
    },
    200: {
        "description": "Successful completion of the request.",
        "content": {
            "application/json": {
                "example": {
                    "details": "user updated successfully",
                    
                },
                "example": {
                    "User": "the user data",
                    
                
                    
                },
                "example": {
                    "details": "user deleted successfully",
                    
                
                    
                },
            }
        }
    }
}

video_responses = {
    # Add video-specific error responses here
}

session_responses = {
    # Add session-specific error responses here
}
