from typing import Annotated
from uuid import UUID

from fastapi import Depends

from src.backgrounds.tasks import register_package
from src.packages.cache.package_status import PackageStatusCacheDep, PackageStatusDict
from src.packages.exceptions.package import PackageTypeNotExistsError
from src.packages.models import Package
from src.packages.repositories.package import PackageRepositoryDep
from src.packages.repositories.package_type import PackageTypeRepositoryDep
from src.packages.schemas.package import PackageFilterOptions, PackageIn, PackageOut
from src.packages.schemas.package_status import PackageStatusUUIDOut
from src.sessions.models import Session
from src.sessions.repositories.session import SessionRepositoryDep
from src.utils.database import atomic
from src.utils.dependencies import AsyncSessionDep
from src.utils.exceptions import Http404
from src.utils.pagination import PaginationIn, PaginationOut, paginate


class PackageService:
    def __init__(
        self,
        cache: PackageStatusCacheDep,
        db_session: AsyncSessionDep,
        package_repo: PackageRepositoryDep,
        session_repo: SessionRepositoryDep,
        package_type_repo: PackageTypeRepositoryDep,
    ):
        self._cache = cache
        self._db_session = db_session
        self._repo = package_repo
        self._session_repo = session_repo
        self._type_rep = package_type_repo

    async def list_package(
        self, pagination: PaginationIn, filters: PackageFilterOptions, session_id: int
    ) -> PaginationOut[PackageOut]:
        """
        Возвращает страницу списка посылок
        """
        stm = self._repo.list_query(session_id, filters.package_type, filters.has_cost)
        items = await paginate(
            stm, pagination, self._db_session, PackageOut, prefix='packages/'
        )
        return items

    async def get_package(self, package_id: int, session_id: int) -> Package:
        """
        Возвращает посылку пользователя по ID
        """
        package = await self._repo.get(
            package_id, expression=Package.session_id == session_id
        )
        if package is None:
            raise Http404
        return package

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

    async def get_status(
        self, status_uuid: UUID, session: Session
    ) -> PackageStatusDict:
        """
        Возвращает статус посылки по её UUID'у

        Notes:
            После регистрации посылки создаётся её статус,
            который можно отслеживать по выданному UUID'у.
            Поскольку регистрация происходит удалённо, по статусу
            посылки можно отследить, прошла ли она успешно, а также
            получить ID зарегистрированной посылки

        Returns:
            Статус посылки - регистрация ли прошла успешно + ID зарегистрированной посылки
        """
        status = await self._cache.get_status(session.id, status_uuid)
        return status


PackageServiceDep = Annotated[PackageService, Depends()]
