import config
from fastapi import FastAPI
from adapters import handlers
from dishka.integrations.fastapi import setup_dishka, FastapiProvider
from dishka import make_async_container
from ioc import FastApiApp
from config import Config
from pydantic import ValidationError
from adapters import exceptions
config = Config()
print(config)
container = make_async_container(FastApiApp(), FastapiProvider(), context={Config: config})
def get_fastapi_app() -> FastAPI:

    app = FastAPI()

    for exc_type, handler in exceptions.all_exceptions.items():
        app.add_exception_handler(exc_type, handler)
        
    app.include_router(handlers.router)
    setup_dishka(container, app)
    return app

def get_app(config: Config) -> FastAPI:
    print(config)
    fastapi = get_fastapi_app()
    
    return fastapi

app = get_app(config)