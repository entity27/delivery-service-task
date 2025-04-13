from uuid import UUID

from pydantic import BaseModel


class PackageStatusUUIDOut(BaseModel):
    """
    UUID для получения статуса посылки, выдаётся при регистрации
    """

    uuid: UUID


class PackageStatusOut(BaseModel):
    """
    Статус посылки, отражает успех её регистрации

    Attributes:
        pending: Посылка находится в обработке (или обработка завершена)
        error: Во время регистрации произошла ошибка
        id: ID зарегистрированной посылки, назначается после успешной регистрации
    """

    pending: bool
    error: bool
    id: int | None
