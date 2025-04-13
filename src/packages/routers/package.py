from fastapi import APIRouter, status

from src.packages.schemas.package import PackageIn
from src.packages.schemas.package_status import PackageStatusUUIDOut
from src.packages.services.package import PackageServiceDep
from src.sessions.dependencies.cookie import SessionCookieDep
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
    responses=generate_custom_error_responses([SessionCookieRequiredError]),
)
async def package_create(
    package: PackageIn, session_token: SessionCookieDep, service: PackageServiceDep
) -> PackageStatusUUIDOut:
    return await service.register(package, session_token)
