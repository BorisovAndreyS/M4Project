from celery import Celery


from app.config import settings

celery_app = Celery(
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=['app.tasks']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_pool='solo',
    beat_schedule={
        'parse_news': {
            'task': 'parse_news',
            'schedule': settings.PARSE_INTERVAL_MINUTES * 60,
       },
    }
)

if __name__ == '__main__':
    celery_app.start()