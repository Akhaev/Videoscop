from os import environ as env

from pydantic import Field, BaseModel


class PostgresConfig(BaseModel):
    host: str = Field(alias='POSTGRES_HOST', default='127.0.0.1')
    port: int = Field(alias='POSTGRES_PORT', default='5432')
    login: str = Field(alias='POSTGRES_USER', default='postgres')
    password: str = Field(alias='POSTGRES_PASSWORD', default='password')
    database: str = Field(alias='POSTGRES_DB', default='postgres')

class FastApiConfig(BaseModel):
    pass

class Config(BaseModel):
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
    fastapi: FastApiConfig = Field(default_factory=lambda: FastApiConfig(**env))