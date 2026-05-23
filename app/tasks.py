from celery_worker import celery_app
import logging
from datetime import datetime

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from celery_worker import celery_app
from app.db.models import NewsItem
from app.db.db import sync_session_factory
from app.news_parser.sites import HabrParser


logger = logging.getLogger(__name__)


@celery_app.task(
    name='parse_news',
    bind=True,
    max_retries=3,
    autoretry_for=(Exception,),
    retry_kwargs={'countdown': 60})

def parse_news(self, source: str = 'habr', limit: int = 10):
    """
        Запускает парсер для источника и сохраняет новости в БД.
    """
    try:
        logger.info('Parsing news...')

        parser = HabrParser()

        articles = parser.parse()

        logger.info(f"Найдено {len(articles)} новостей")

        saved = 0
        skipped = 0

        with sync_session_factory() as session:
            for item in articles[:limit]:
                #Проверка дубликата
                stmt = select(NewsItem).where(NewsItem.url == item['url'])
                result = session.execute(stmt)
                existing = result.scalar_one_or_none()
                if existing:
                    logger.info("Данная статья уже есть")
                    skipped += 1
                    continue
                #Вставка статьи
                news = NewsItem(
                    url=item['url'],
                    title=item['title'],
                    source=source,
                    summary=item['summary'],
                    published_at=item['published_at'],
                )
                session.add(news)
                saved += 1

            session.commit()
            logger.info(f'Сохранено {saved} новостей, пропущено {skipped}')
            return {"status": "success", "saved": saved, "skipped": skipped}

    except Exception as e:
        logger.error(f"Ошибка при сохранении данных: {e}", exc_info=True)
        raise self.retry(exc=e)
