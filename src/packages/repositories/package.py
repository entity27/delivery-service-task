from typing import Annotated

from fastapi import Depends

from src.packages.models import Package
from src.utils.repository import BaseRepository


class PackageRepository(BaseRepository[Package]):
    model = Package


PackageRepositoryDep = Annotated[PackageRepository, Depends()]
