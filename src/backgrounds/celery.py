from celery import Celery

from src.config.settings import settings

app = Celery(
    main='delivery',
    broker=settings.celery_broker_url,
    backend=settings.celery_results_url,
)
app.conf.update(
    task_routes={
        'src.backgrounds.tasks.register_package.register_package': {
            'queue': 'register_package'
        },
    }
)
app.autodiscover_tasks(packages=['src.backgrounds'])
app.autodiscover_tasks()
