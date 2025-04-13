from collections.abc import Sequence

from fastapi import APIRouter, status

from src.packages.schemas.package_type import PackageTypeOut
from src.packages.services.package_type import PackageTypeServiceDep

router = APIRouter(tags=['Типы посылок'])


@router.get(
    path='/',
    response_model=Sequence[PackageTypeOut],
    status_code=status.HTTP_200_OK,
    summary='Список всех типов посылок в системе',
    description='Набор всех типов посылок в БД без пагинации',
)
async def types_list(service: PackageTypeServiceDep) -> Sequence[PackageTypeOut]:
    return await service.list()
