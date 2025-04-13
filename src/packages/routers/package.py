from uuid import UUID

from fastapi import APIRouter, status

from src.packages.cache.package_status import PackageStatusDict
from src.packages.exceptions.package import PackageTypeNotExistsError
from src.packages.exceptions.package_status import (
    PackageStatusDecodeError,
    PackageStatusNotFoundError,
)
from src.packages.schemas.package import PackageIn
from src.packages.schemas.package_status import PackageStatusOut, PackageStatusUUIDOut
from src.packages.services.package import PackageServiceDep
from src.sessions.dependencies.cookie import SessionCookieDep
from src.sessions.dependencies.session import SessionDep
from src.sessions.exceptions.cookie import SessionCookieRequiredError
from src.utils.exceptions import generate_custom_error_responses

router = APIRouter(tags=['Посылки'])


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
