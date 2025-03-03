import config
from fastapi import FastAPI
from adapters import handlers
from dishka.integrations.fastapi import setup_dishka, FastapiProvider
from dishka import make_async_container
from ioc import FastApiApp
from config import Config

config = Config()
container = make_async_container(FastApiApp(), FastapiProvider(), context={Config: config})
def get_fastapi_app(config):

    app = FastAPI()

    app.include_router(handlers.router)
    setup_dishka(container, app)
    return app

def get_app():
    fastapi = get_fastapi_app(config.FastApiConfig)
    
    return fastapi