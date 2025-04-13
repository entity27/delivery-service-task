from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends

from src.packages.repositories.package_type import PackageTypeRepositoryDep
from src.packages.schemas.package_type import PackageTypeOut


class PackageTypeService:
    def __init__(
        self,
        package_type_repo: PackageTypeRepositoryDep,
    ):
        self._repo = package_type_repo

    async def list(self) -> Sequence[PackageTypeOut]:
        result = await self._repo.list(ignore_pagination=True)
        return [
            PackageTypeOut.model_validate(item, from_attributes=True) for item in result
        ]


PackageTypeServiceDep = Annotated[PackageTypeService, Depends()]
