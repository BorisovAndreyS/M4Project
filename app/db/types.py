import uuid
from datetime import datetime
from enum import StrEnum, Enum

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.annotation import Annotated


class PostStatus(StrEnum):
    NEW = "new"
    GENERATED = "generated"
    PUBLISHED = "published"
    FAILED = "failed"


class SourceType(Enum):
    SITE = "site"
    tg = "tg"


ID = Annotated[int, Column(String,
                           primary_key=True,
                           index=True,
                           default=uuid.uuid4)]

URL = Annotated[str, Column(String, nullable=False, index=True)]
TextContent = Annotated[str, Column(String, nullable=True, index=True)]
TimeStamp = Annotated[datetime, Column(DateTime, nullable=False, index=True, default=datetime.now)]

STATUS_POST = Annotated[PostStatus, Column(Enum(PostStatus), nullable=False)]

SOURCE_TYPE = Annotated[SourceType, Column(Enum(SourceType), nullable=False)]
