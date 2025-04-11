import pytest
from httpx import AsyncClient

from src.utils.responses import OkResponse


@pytest.mark.asyncio(loop_scope='session')
async def test_dummy(client: AsyncClient) -> None:
    """
    Проверяем, что заготовка под тесты работает
    """
    test = await client.get('/packages/')
    assert test.status_code == 200
    assert test.json() == OkResponse().model_dump()
