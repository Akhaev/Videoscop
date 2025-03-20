from . import schemas
import datetime
from datetime import timezone
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
    'create': {
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
        201: {
            "description": "Successful authentication, returns the access token.",
            "content": {
                "application/json": {
                    "example": {
                        "token": "user token for authentication",
                    }
                }
            }
        }
    },
    'update': {
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
        404: {
            "description": "Not Found: The authenticated or requested user was not found.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User not found",
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
                    }
                }
            }
        }
    },
    'get': {
        404: {
            "description": "Not Found: The authenticated or requested user was not found.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User not found",
                    }
                }
            }
        },
        200: {
            "description": "Successful completion of the request.",
            "content": {
                "application/json": {
                    "example": {
                        "User": 'user data',
                    }
                }
            }
        }
    },
    'delete': {
        404: {
            "description": "Not Found: The authenticated or requested user was not found.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User not found",
                    }
                }
            }
        },
        200: {
            "description": "Successful completion of the request.",
            "content": {
                "application/json": {
                    "example": {
                        "details": "user deleted successfully",
                    }
                }
            }
        }
    }
}

video_responses = {
    'search': {
        200: {
            "description": "Successful completion of the request.",
            "content": {
                "application/json": {
                    "example": {
                        "videos": '[videos]'
                    },
                },
            },
        },
        422: {
            "description": "Validation error: some fields contain incorrect data.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "incorrect field/fields",
                        "problem_fields": {
                            "date": "invalid date format",
                        }
                    }
                }
            }
        }
    }
}

session_responses = {
    # Add session-specific error responses here
}
