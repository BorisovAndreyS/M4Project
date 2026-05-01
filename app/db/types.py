import uuid
from datetime import datetime
from enum import StrEnum, Enum

from sqlalchemy import Column, String, DateTime, Enum, func, Text
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.sql.annotation import Annotated


class PostStatus(StrEnum):
    NEW = "new"
    GENERATED = "generated"
    PUBLISHED = "published"
    FAILED = "failed"


class SourceType(StrEnum):
    SITE = "site"
    tg = "tg"


ID = Annotated[int, mapped_column(primary_key=True, index=True, default=uuid.uuid4)]
URL = Annotated[str, mapped_column(String(2048), nullable=False)]
TextContent = Annotated[str | None, mapped_column(Text, nullable=True)]
TimeStamp = Annotated[datetime, mapped_column(DateTime, nullable=False, server_default=func.now())]

# STATUS_POST = Annotated[PostStatus, mapped_column(Enum(PostStatus), nullable=False)]
# SOURCE_TYPE = Annotated[SourceType, mapped_column(Enum(SourceType), nullable=False)]
