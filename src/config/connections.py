from redis.asyncio import ConnectionPool
from sqlalchemy.ext.asyncio import create_async_engine

from src.config.settings import settings

# Engine для получения БД сессии
engine_async = create_async_engine(settings.sqlalchemy_async_url)

# Redis pool подключений
redis_pool = ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASS,
    decode_responses=True,
)
