from asyncio import get_event_loop

from src.backgrounds.celery import app
from src.utils.dependencies import get_session_async


@app.task(retry_backoff=True, max_retries=4, default_retry_delay=4, rate_limit='666/m')  # type: ignore[misc]
def some_task() -> None:
    """
    Заглушка под Celery задачу
    """
    get_event_loop().run_until_complete(_task())


async def _task() -> None:
    async for _ in get_session_async():
        print('малютка работает')
