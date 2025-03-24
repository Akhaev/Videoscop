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
                        "videos": "[video1_data, video2_data]",
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
        },
        404: {
            "description": "Not Found: The authenticated user was not found.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User not found",
                    }
                }
            }
        },
    },
    'create': {
        201: {
            "description": "Video created successfully, returns an upload link.",
            "content": {
                "application/json": {
                    "example": {
                        "upload_link": "https://example.com/upload/video.mp4"
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized: User authentication failed.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Authorization token is missing or improperly formatted"
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
                            "name": "Name must be between 3 and 50 characters",
                            "length_seconds": "Length must be between 1 and 3600 seconds",
                            "size": "Size must be an integer between 1 and 1000 MB"
                        }
                    }
                }
            }
        },
        409: {
            "description": "Conflict: A video with the same name already exists for this author.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Conflict field/fields",
                        "problem_fields": {
                            "name": "already exists for this author"
                        }
                    }
                }
            }
        },
        404: {
            "description": "Not Found: The authenticated user was not found.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User not found",
                    }
                }
            }
        }
    }
}

heat_map_responses = {
    'create': {
        201: {
            "description": "Heat map created successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "details": "heat map created successfully",
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized: User authentication failed.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Authorization token is missing or improperly formatted"
                    }
                }
            }
        },
        409: {
            "description": "Conflict: The video already has a heat map.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Conflict field/fields",
                        "problem_fields": {
                            "video": "already has a heat map"
                        }
                    }
                }
            }
        },
        404: {
            "description": "Not Found: The authenticated user was not found or video with this name not found.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User not found",
                    },
                    "example": {
                        "message": "video with this not found",
                    }
                }
            }
        },
        422: {
            "description": "Validation error: video name is invalid.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "incorrect field/fields",
                        "problem_fields": {
                            "video_name": "Name must be between 3 and 50 characters"
                        }
                    }
                }
            }
        }
    }
}