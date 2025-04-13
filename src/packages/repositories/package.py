from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy import Select, and_, select

from src.packages.models import Package
from src.utils.repository import BaseRepository


class PackageRepository(BaseRepository[Package]):
    model = Package

    def list_query(
        self,
        session_id: int,
        package_type: int | None = None,
        has_cost: bool | None = None,
    ) -> Select[Any]:
        """
        Возвращает statement списка по сессии с фильтрацией
        """
        stm = select(self.model)

        where_clause = Package.session_id == session_id
        if package_type is not None:
            where_clause = and_(where_clause, Package.package_type_id == package_type)
        if has_cost is False:
            where_clause = and_(where_clause, Package.cost.is_(None))
        elif has_cost is True:
            where_clause = and_(where_clause, Package.cost.is_not(None))

        stm = stm.where(where_clause)
        stm = stm.order_by(self.model.id.desc())
        return stm


PackageRepositoryDep = Annotated[PackageRepository, Depends()]
