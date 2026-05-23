import asyncio
from app.tasks import parse_news

async def main():
    result = await parse_news.run(source='habr', limit=2)
    print(f"Результат: {result}")

asyncio.run(main())