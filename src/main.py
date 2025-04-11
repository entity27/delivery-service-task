from fastapi import FastAPI

from src.config.settings import settings
from src.routes import router

app = FastAPI(
    title='Delivery Service',
    debug=settings.DEBUG,
)

app.include_router(router)
