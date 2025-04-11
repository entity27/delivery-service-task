from celery import Celery
from celery.schedules import crontab

from src.config.settings import settings

app = Celery(
    main='delivery',
    broker=settings.celery_broker_url,
    backend=settings.celery_results_url,
)
app.conf.update(
    task_routes={
        'src.backgrounds.tasks.some_task.some_task': {'queue': 'some_task'},
    }
)
app.conf.beat_schedule = {
    'some_task': {
        'task': 'src.backgrounds.tasks.some_task.some_task',
        'schedule': crontab(minute='*/1'),
    },
}
app.autodiscover_tasks(packages=['src.backgrounds'])
app.autodiscover_tasks()
