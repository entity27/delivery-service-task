from typing import Annotated

from fastapi import Depends

from src.backgrounds.tasks import register_package
from src.packages.cache.package_status import PackageStatusCacheDep
from src.packages.exceptions.package import PackageTypeNotExistsError
from src.packages.repositories.package_type import PackageTypeRepositoryDep
from src.packages.schemas.package import PackageIn
from src.packages.schemas.package_status import PackageStatusUUIDOut
from src.sessions.repositories.session import SessionRepositoryDep
from src.utils.database import atomic
from src.utils.dependencies import AsyncSessionDep


class PackageService:
    def __init__(
        self,
        cache: PackageStatusCacheDep,
        db_session: AsyncSessionDep,
        session_repo: SessionRepositoryDep,
        package_type_repo: PackageTypeRepositoryDep,
    ):
        self._cache = cache
        self._db_session = db_session
        self._session_repo = session_repo
        self._type_rep = package_type_repo

    async def register(
        self, package: PackageIn, session_token: str
    ) -> PackageStatusUUIDOut:
        """
        Производим удалённую регистрацию посылки

        Args:
            package: Данные о посылке
            session_token: Сессия пользователя
        """
        if not await self._type_rep.exists(package.package_type_id):
            raise PackageTypeNotExistsError

        async with atomic(self._db_session):
            session = await self._session_repo.get_or_create(session_token)
            status_uuid = await self._cache.new_status(session.id)

        register_package.delay(
            data=package.model_dump(by_alias=True),
            session_id=session.id,
            status_uuid=status_uuid,
        )

        return PackageStatusUUIDOut(uuid=status_uuid)


PackageServiceDep = Annotated[PackageService, Depends()]
