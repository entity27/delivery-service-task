from pydantic import BaseModel, ConfigDict


class PackageTypeOut(BaseModel):
    """
    Получение типа посылки
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
