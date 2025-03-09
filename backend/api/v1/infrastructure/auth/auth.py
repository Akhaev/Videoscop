
from application import interfaces
from fastapi import Request
from config import JWTConfig    
import jwt
from datetime import datetime, timedelta
from . import exceptions 

class Auth(interfaces.AuthAdd):
    def __init__(self, request: Request, config: JWTConfig) -> str:
        self.request = request
        self.config = config
    def add(self, user_id: str) -> interfaces.Token:
        now = datetime.now()
        payload = {
            "sub": user_id,
            "exp": now + timedelta(days=self.config.expiration_days),
            "nbf": now,
            "iat": now,
        }

        token = jwt.encode(payload, self.config.secret_key, algorithm="HS256")
        return token
    def current_user(self) -> str:

        auth_header = self.request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise exceptions.UnAuthorizedError()

        token = auth_header.split(" ")[1]
        print(token)
        payload = jwt.decode(
            token,
            self.config.secret_key,
            algorithms=["HS256"],
            options={"require": ["exp", "nbf", "iat"]},
            )

        return payload.get("sub")
