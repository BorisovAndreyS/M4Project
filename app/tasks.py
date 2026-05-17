from celery_worker import celery_app
import logging
from datetime import datetime

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from celery_worker import celery_app
from db.models import NewsItem, Source
from db.db import async_session


logger = logging.getLogger(__name__)


@celery_app.task(name='parse_news')
def parse_news():
    logger.info('Parsing news...')

