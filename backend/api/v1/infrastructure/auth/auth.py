
from application import interfaces
from fastapi import Request
from config import JWTConfig    
import jwt
from datetime import datetime, timedelta, timezone
from . import exceptions 
 
now = datetime.now(timezone.utc) + timedelta(hours=3)

 
class Auth(interfaces.AuthAdd):
    def __init__(self, request: Request, config: JWTConfig) -> str:
        self.request = request
        self.config = config
    def add(self, user_id: str) -> interfaces.Token:
        payload = {
            "sub": user_id,
            "exp": now + timedelta(days=self.config.expiration_days),
            "nbf": now,
            "iat": now,
        }

        token = jwt.encode(payload, self.config.secret_key, algorithm="HS256")
        return token
    def current_user(self) -> str | None:

        auth_header = self.request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        payload = jwt.decode(
            token,
            self.config.secret_key,
            algorithms=["HS256"],
            options={"require": ["exp", "nbf", "iat"]},
            )

        return payload.get("sub")
