from celery_worker import celery_app
import logging


logger = logging.getLogger(__name__)


@celery_app.task(name='parse_news')
def parse_news():
    print('Parsing news...')
    logger.info('Parsing news...')
