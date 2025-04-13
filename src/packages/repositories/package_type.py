from typing import Annotated

from fastapi import Depends

from src.packages.models import PackageType
from src.utils.repository import BaseRepository


class PackageTypeRepository(BaseRepository[PackageType]):
    model = PackageType


PackageTypeRepositoryDep = Annotated[PackageTypeRepository, Depends()]
