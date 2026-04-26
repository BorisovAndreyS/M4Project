import uuid
from datetime import datetime
from enum import StrEnum, Enum

from starlette.datastructures import URL

from .types import TimeStamp, TextContent, ID, STATUS_POST, SOURCE_TYPE
from pyparsing import Optional
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.annotation import Annotated

Base = declarative_base()


class NewsItem(Base):
    __tablename__ = "news_items"

    id: ID
    title: str = Column(String, nullable=False, index=True)
    url: Optional[URL]
    summary: TextContent
    source: str = Column(String, nullable=False)
    published_at: TimeStamp
    raw_text: Optional[TextContent]
    created_at: TimeStamp


class Post(Base):
    __tablename__ = "posts"

    id: ID
    news_id:  ID
    generated_text: TextContent
    published_at: TimeStamp
    status: STATUS_POST
    created_at: TimeStamp

class Source(Base):
    __tablename__ = "sources"
    
    id: ID
    type: SOURCE_TYPE
    name: str = Column(String, nullable=False)
    url: URL
    enabled: bool