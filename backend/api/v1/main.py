import config
from fastapi import FastAPI
from adapters.handlers import user, video
from dishka.integrations.fastapi import setup_dishka, FastapiProvider
from dishka import make_async_container
from ioc import FastApiApp
from config import Config
from adapters import exceptions_handlers
config = Config()

container = make_async_container(FastApiApp(), FastapiProvider(), context={Config: config})
def get_fastapi_app() -> FastAPI:

    app = FastAPI()

    for exc_type, handler in exceptions_handlers.all_handlers.items():
        app.add_exception_handler(exc_type, handler)
        
    app.include_router(user.router)
    app.include_router(video.router)
    setup_dishka(container, app)
    return app

def get_app(config: Config) -> FastAPI:
    fastapi = get_fastapi_app()
    
    return fastapi

app = get_app(config)