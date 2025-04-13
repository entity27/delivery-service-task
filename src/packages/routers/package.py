from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Path, status
from fastapi.params import Depends

from src.packages.cache.package_status import PackageStatusDict
from src.packages.exceptions.package import PackageTypeNotExistsError
from src.packages.exceptions.package_status import (
    PackageStatusDecodeError,
    PackageStatusNotFoundError,
)
from src.packages.models import Package
from src.packages.schemas.package import PackageFilterOptions, PackageIn, PackageOut
from src.packages.schemas.package_status import PackageStatusOut, PackageStatusUUIDOut
from src.packages.services.package import PackageServiceDep
from src.sessions.dependencies.cookie import SessionCookieDep
from src.sessions.dependencies.session import SessionDep
from src.sessions.exceptions.cookie import SessionCookieRequiredError
from src.utils.exceptions import Http404, generate_custom_error_responses
from src.utils.pagination import PaginationIn, PaginationOut

router = APIRouter(tags=['Посылки'])


@router.get(
    path='/',
    response_model=PaginationOut[PackageOut],
    status_code=status.HTTP_200_OK,
    summary='Получение списка посылок',
    description='Список посылок с пагинацией и фильтрацией',
    responses=generate_custom_error_responses([Http404]),
)
async def package_list(
    pagination: Annotated[PaginationIn, Depends()],
    filters: Annotated[PackageFilterOptions, Depends()],
    session: SessionDep,
    service: PackageServiceDep,
) -> PaginationOut[PackageOut]:
    return await service.list_package(pagination, filters, session.id)


@router.get(
    path='/{package_id}/',
    response_model=PackageOut,
    status_code=status.HTTP_200_OK,
    summary='Детальное получение объекта посылки',
    description='Получает детальку посылки по ID',
    responses=generate_custom_error_responses([Http404]),
)
async def package_get(
    package_id: Annotated[int, Path(gt=0)],
    session: SessionDep,
    service: PackageServiceDep,
) -> Package:
    return await service.get_package(package_id, session.id)


@router.post(
    path='/',
    response_model=PackageStatusUUIDOut,
    status_code=status.HTTP_201_CREATED,
    summary='Регистрация посылки',
    description='Производит отложенную регистрацию посылки, возвращает её статус. '
    'Регистрация будет производиться celery воркером через rabbitmq брокер',
    responses=generate_custom_error_responses(
        [
            SessionCookieRequiredError,
            PackageTypeNotExistsError,
        ]
    ),
)
async def package_create(
    package: PackageIn, session_token: SessionCookieDep, service: PackageServiceDep
) -> PackageStatusUUIDOut:
    return await service.register(package, session_token)


@router.get(
    path='/status/{status_uuid}/',
    response_model=PackageStatusOut,
    status_code=status.HTTP_200_OK,
    summary='Получение статуса посылки',
    description='Выдаёт статус посылки - завершилась ли регистрация, или нет. Произошла ли ошибка во время регистрации',
    responses=generate_custom_error_responses(
        [
            PackageStatusNotFoundError,
            PackageStatusDecodeError,
        ]
    ),
)
async def package_status(
    status_uuid: UUID, session: SessionDep, service: PackageServiceDep
) -> PackageStatusDict:
    return await service.get_status(status_uuid, session)
