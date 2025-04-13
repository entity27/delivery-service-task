from collections.abc import Sequence
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import BinaryExpression, exists, select
from sqlalchemy.sql.base import ExecutableOption

from src.utils.dependencies import AsyncSessionDep
from src.utils.models import IDModel

ModelT = TypeVar('ModelT', bound=IDModel)


class BaseRepository(Generic[ModelT]):
    model: type[ModelT] = NotImplemented

    def __init__(self, db_session: AsyncSessionDep):
        """
        Репозиторий взаимодействия с БД, реализующий базовые операции (CRUD)

        Args:
            db_session: Сессия БД
        """
        self._session = db_session

    async def list(
        self,
        offset: int = 0,
        limit: int = 100,
        expression: BinaryExpression[ModelT] | None = None,
        ignore_pagination: bool = False,
        *options: ExecutableOption,
    ) -> Sequence[ModelT]:
        """
        Возвращает список объектов

        Args:
            offset: Пропуск элементов
            limit: Лимит элементов
            expression: Дополнительные условия
            ignore_pagination: Если True - не применяет offset и limit к запросу
            *options: Дополнительные опции
        """
        stm = select(self.model)

        if expression is not None:
            stm = stm.where(expression)
        if ignore_pagination is False:
            stm = stm.offset(offset).limit(limit)

        stm = stm.order_by(self.model.id.desc())

        if options:
            stm = stm.options(*options)

        results = await self._session.execute(stm)
        return results.scalars().all()

    async def get(
        self, item_id: int, expression: BinaryExpression[ModelT] | None = None
    ) -> ModelT | None:
        """
        Возвращает объект, если существует

        Args:
            item_id: ID объекта
            expression: Дополнительные условия
        """
        where_clause = self.model.id == item_id
        if expression is not None:
            where_clause &= expression

        statement = select(self.model).where(where_clause)
        return (await self._session.execute(statement)).scalar_one_or_none()

    async def create(self, item: ModelT) -> ModelT:
        """
        Создаёт объект

        Args:
            item: Объект
        """
        self._session.add(item)
        await self._session.flush()
        return item

    async def create_from_pydantic(self, data: BaseModel) -> ModelT:
        """
        Создаёт объект из pydantic схемы

        Args:
            data: BaseModel
        """
        item: ModelT = self.model(**data.model_dump())
        self._session.add(item)
        await self._session.flush()
        return item

    async def update(self, item: ModelT) -> ModelT:
        """
        Обновляет объект

        Args:
            item: Объект
        """
        self._session.add(item)
        await self._session.flush()
        return item

    async def delete(self, item: ModelT) -> None:
        """
        Удаляет объект

        Args:
            item: Объект
        """
        await self._session.delete(item)
        await self._session.flush()

    async def exists(self, item_id: int) -> bool:
        """
        Проверяет, что объект по указанному ID существует
        """
        stm = select(exists().where(self.model.id == item_id))
        result = await self._session.scalar(stm)
        return result or False
