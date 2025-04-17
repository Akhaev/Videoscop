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
                    "examples": {
                        "Email Exists": {
                            "value": {
                                "message": "conflict field/fields",
                                "problem_fields": {
                                    "email": "already exists",
                                }
                            }
                        }
                    }
                }
            }
        },
        422: {
            "description": "Validation error: some fields contain incorrect data.",
            "content": {
                "application/json": {
                    "examples": {
                        "Invalid Email": {
                            "value": {
                                "message": "incorrect field/fields",
                                "problem_fields": {
                                    "email": "invalid email format",
                                    "password": "password must be at least 8 characters long"
                                }
                            }
                        }
                    }
                }
            }
        },
        201: {
            "description": "Successful authentication, returns the access token.",
            "content": {
                "application/json": {
                    "examples": {
                        "Success": {
                            "value": {
                                "token": "user token for authentication",
                            }
                        }
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
                    "examples": {
                        "Email Exists": {
                            "value": {
                                "message": "conflict field/fields",
                                "problem_fields": {
                                    "email": "already exists",
                                }
                            }
                        }
                    }
                }
            }
        },
        422: {
            "description": "Validation error: some fields contain incorrect data.",
            "content": {
                "application/json": {
                    "examples": {
                        "Invalid Email": {
                            "value": {
                                "message": "incorrect field/fields",
                                "problem_fields": {
                                    "email": "invalid email format",
                                    "password": "password must be at least 8 characters long"
                                }
                            }
                        }
                    }
                }
            }
        },
        400: {
            "description": "Bad Request: The request could not be understood or was missing required parameters.",
            "content": {
                "application/json": {
                    "examples": {
                        "Missing Password": {
                            "value": {
                                "message": "requires an up-to-date password to update password or email",
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Not Found: The authenticated or requested user was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "User Not Found": {
                            "value": {
                                "message": "User not found",
                            }
                        }
                    }
                }
            }
        },
        200: {
            "description": "Successful completion of the request.",
            "content": {
                "application/json": {
                    "examples": {
                        "Success": {
                            "value": {
                                "details": "user updated successfully",
                            }
                        }
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
                    "examples": {
                        "User Not Found": {
                            "value": {
                                "message": "User not found",
                            }
                        }
                    }
                }
            }
        },
        200: {
            "description": "Successful completion of the request.",
            "content": {
                "application/json": {
                    "examples": {
                        "Success": {
                            "value": {
                                "User": 'user data',
                            }
                        }
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
                    "examples": {
                        "User Not Found": {
                            "value": {
                                "message": "User not found",
                            }
                        }
                    }
                }
            }
        },
        200: {
            "description": "Successful completion of the request.",
            "content": {
                "application/json": {
                    "examples": {
                        "Success": {
                            "value": {
                                "details": "user deleted successfully",
                            }
                        }
                    }
                }
            }
        }
    },
    'generate_token': {
        201: {
            "description": "Successful generation of a new token.",
            "content": {
                "application/json": {
                    "examples": {
                        "Success": {
                            "value": {
                                "token": "new user token for authentication",
                            }
                        }
                    }
                }
            }
        },
        422: {
            "description": "Validation error: some fields contain incorrect data.",
            "content": {
                "application/json": {
                    "examples": {
                        "Invalid password": {
                            "value": {
                                "message": "incorrect field/fields",
                                "problem_fields": {
                                    "password": "invalid password format"
                                }
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Not found: password or login\email dont exists.",
            "content": {
                "application/json": {
                    "examples": {
                        "Password or login\email dont exists": {
                            "value": {
                                "message": "User not found",
                            }
                        }
                    }
                }
            }
        },
    }
}

video_responses = {
    'search': {
        200: {
            "description": "Successful completion of the request.",
            "content": {
                "application/json": {
                    "examples": {
                        "Success": {
                            "value": {
                                "videos": "[videos, cursor]",
                            }
                        }
                    }
                }
            }
        },
        422: {
            "description": "Validation error: some fields contain incorrect data.",
            "content": {
                "application/json": {
                    "examples": {
                        "Invalid Date": {
                            "value": {
                                "message": "incorrect field/fields",
                                "problem_fields": {
                                    "date": "invalid date format",
                                }
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Not Found: The authenticated user was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "User Not Found": {
                            "value": {
                                "message": "User not found",
                            }
                        }
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
                    "examples": {
                        "Success": {
                            "value": {
                                "upload_link": "https://example.com/upload/video.mp4"
                            }
                        }
                    }
                }
            }
        },
        422: {
            "description": "Validation error: some fields contain incorrect data.",
            "content": {
                "application/json": {
                    "examples": {
                        "Invalid Fields": {
                            "value": {
                                "message": "incorrect field/fields",
                                "problem_fields": {
                                    "name": "Name must be between 3 and 50 characters",
                                    "length_seconds": "Length must be between 1 and 3600 seconds",
                                    "size": "Size must be an integer between 1 and 1000 MB"
                                }
                            }
                        }
                    }
                }
            }
        },
        409: {
            "description": "Conflict: A video with the same name already exists for this author or video already uploaded.",
            "content": {
                "application/json": {
                    "examples": {
                        "Name Conflict": {
                            "value": {
                                "message": "Conflict field/fields",
                                "problem_fields": {
                                    "name": "already exists for this author"
                                }
                            }
                        },
                        "File Exists": {
                            "value": {
                                "message": "File 'file_name' already exists",
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Not Found: The authenticated user was not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "User Not Found": {
                            "value": {
                                "message": "User not found",
                            }
                        }
                    }
                }
            }
        }
    },
    'get_unload_link': {
        200: {
            "description": "Successful completion of the request.",
            "content": {
                "application/json": {
                    "examples": {
                        "Success": {
                            "value": {
                                "unload_link": "https://example.com/unload/video.mp4"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Not Found: The authenticated user was not found or video not uploaded or not created.",
            "content": {
                "application/json": {
                    "examples": {
                        "User Not Found": {
                            "value": {
                                "message": "User not found",
                            }
                        },
                        "Video Not Found": {
                            "value": {
                                "message": "Video not found",
                            }
                        },
                        "File Not Exists": {
                            "value": {
                                "message": "File 'video_name' does not exist",
                            }
                        }
                    }
                }
            }
        },
        422: {
            "description": "Validation error: video name is invalid.",
            "content": {
                "application/json": {
                    "examples": {
                        "Invalid Video Name": {
                            "value": {
                                "message": "incorrect field/fields",
                                "problem_fields": {
                                    "video_name": "Name must be between 3 and 50 characters"
                                }
                            }
                        }
                    }
                }
            }
        },
    }
}

heat_map_responses = {
    'create': {
        201: {
            "description": "Heat map created successfully, returns an upload link.",
            "content": {
                "application/json": {
                    "examples": {
                        "Success": {
                            "value": {
                                "upload_link": "https://example.com/upload/heatmap.mp4"
                            }
                        }
                    }
                }
            }
        },
        409: {
            "description": "Conflict: The video already has a heat map or heatmap already uploaded.",
            "content": {
                "application/json": {
                    "examples": {
                        "Heatmap Exists": {
                            "value": {
                                "message": "Conflict field/fields",
                                "problem_fields": {
                                    "video": "already has a heat map"
                                }
                            }
                        },
                        "File Exists": {
                            "value": {
                                "message": "File 'file_name' already exists",
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Not Found: The authenticated user was not found or video not found.",
            "content": {
                "application/json": {
                    "examples": {
                        "User Not Found": {
                            "value": {
                                "message": "User not found",
                            }
                        },
                        "Video Not Found": {
                            "value": {
                                "message": "Video not found",
                            }
                        }
                    }
                }
            }
        },
        422: {
            "description": "Validation error: video name is invalid.",
            "content": {
                "application/json": {
                    "examples": {
                        "Invalid Video Name": {
                            "value": {
                                "message": "incorrect field/fields",
                                "problem_fields": {
                                    "video_name": "Name must be between 3 and 50 characters"
                                }
                            }
                        }
                    }
                }
            }
        },
    },
    'get_unload_link': {
        200: {
            "description": "Successful completion of the request.",
            "content": {
                "application/json": {
                    "examples": {
                        "Success": {
                            "value": {
                                "unload_link": "https://example.com/unload/heatmap.mp4"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Not Found: The authenticated user was not found or video not found or heatmap for video not loaded or not created.",
            "content": {
                "application/json": {
                    "examples": {
                        "User Not Found": {
                            "value": {
                                "message": "User not found",
                            }
                        },
                        "Video Not Found": {
                            "value": {
                                "message": "Video not found",
                            }
                        },
                        "Heatmap Not Found": {
                            "value": {
                                "message": "Heatmap not found",
                            }
                        },
                        "File Not Exists": {
                            "value": {
                                "message": "File 'file_name' does not exist",
                            }
                        }
                    }
                }
            }
        },
        422: {
            "description": "Validation error: video name is invalid.",
            "content": {
                "application/json": {
                    "examples": {
                        "Invalid Video Name": {
                            "value": {
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
    }
}
