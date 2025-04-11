from pathlib import Path
from typing import Annotated

from pydantic import (
    AmqpDsn,
    BeforeValidator,
    HttpUrl,
    MySQLDsn,
    RedisDsn,
)
from pydantic_settings import BaseSettings

from src.utils.parsers import parse_nullable_value

# Директория проекта
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

_IntNullable = Annotated[int | None, BeforeValidator(parse_nullable_value)]
_StrNullable = Annotated[str | None, BeforeValidator(parse_nullable_value)]


class Config(BaseSettings):
    # Общие переменные проекта
    DEBUG: bool
    SECRET_KEY: str

    # База данных
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: _IntNullable = None

    # Редис
    REDIS_HOST: str
    REDIS_DB: int = 1
    REDIS_CACHE_EXPIRE_SECONDS: int = 900
    REDIS_PASS: _StrNullable = None
    REDIS_PORT: _IntNullable = None

    # RabbitMQ
    RABBIT_HOST: str
    RABBIT_PORT: _IntNullable = None
    RABBIT_USER: _StrNullable = None
    RABBIT_PASSWORD: _StrNullable = None
    RABBIT_VHOST: _StrNullable = None

    # URL проекта
    HOST_URL: HttpUrl

    @property
    def project_name(self) -> str:
        return BASE_DIR.name

    @property
    def sqlalchemy_async_url(self) -> str:
        """Строим URL для асинхронного подключения к БД"""
        return str(self.__create_sqlalchemy_dsn(sync=False))

    @property
    def sqlalchemy_sync_url(self) -> str:
        """Строим URL для синхронного подключения к БД"""
        return str(self.__create_sqlalchemy_dsn(sync=True))

    @property
    def celery_broker_url(self) -> str:
        """Брокер для Celery"""
        dsn = AmqpDsn.build(
            scheme='amqp',
            username=self.RABBIT_USER,
            password=self.RABBIT_PASSWORD,
            host=self.RABBIT_HOST,
            port=self.RABBIT_PORT,
            path=self.RABBIT_VHOST,
        )
        return str(dsn)

    @property
    def celery_results_url(self) -> str:
        """Результаты Celery"""
        dsn = RedisDsn.build(
            scheme='redis',
            host=self.REDIS_HOST,
            password=self.REDIS_PASS,
            port=self.REDIS_PORT,
            path=str(self.REDIS_DB),
        )
        return str(dsn)

    def __create_sqlalchemy_dsn(self, sync: bool) -> MySQLDsn:
        """
        Создаёт синхронный/асинхронный URI подключения к БД
        """
        if sync:
            scheme = 'mysql+pymysql'
        else:
            scheme = 'mysql+aiomysql'
        return MySQLDsn.build(
            scheme=scheme,
            username=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )


settings = Config()  # type: ignore
