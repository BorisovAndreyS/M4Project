import uuid
from datetime import datetime
from enum import StrEnum, Enum
from typing import Optional
from app.db.types import TimeStamp, TextContent, ID, PostStatus, SourceType, URL
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean, Enum as SQLEnum
from sqlalchemy.orm import declarative_base, relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.annotation import Annotated

class Base(DeclarativeBase):
    pass


class NewsItem(Base):
    __tablename__ = "news_items"

    id: Mapped[str] = mapped_column(nullable=False, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(nullable=True, index=True)
    url: Mapped[Optional[str]] = mapped_column(nullable=True, index=False)
    summary: str = Column(Text)
    source: str = Column(String, nullable=False)
    published_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    raw_text: Mapped[Optional[str]] = Column(Text)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    posts = relationship("Post",
                     back_populates="news_item",
                     cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(nullable=False, primary_key=True, default=uuid.uuid4)
    news_id: Mapped[str] = mapped_column(ForeignKey('news_items.id'), index=True)
    generated_text: Mapped[Optional[str]] = Column(Text)
    published_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    status: Mapped[PostStatus] = mapped_column(SQLEnum(PostStatus, native_enum=False), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)

    news_item: Mapped[Optional["NewsItem"]] = relationship("NewsItem", back_populates="posts")

class Source(Base):
    __tablename__ = "sources"

    id: Mapped[str] = mapped_column(nullable=False, primary_key=True, default=uuid.uuid4)
    type: Mapped[SourceType] = mapped_column(SQLEnum(SourceType, native_enum=False), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[Optional[str]] = mapped_column(nullable=True, index=False)
    enabled: bool = Column(Boolean, nullable=False, default=True)

class Keyword(Base):
    __tablename__ = "keywords"

    id: Mapped[str] = mapped_column(nullable=False, primary_key=True, default=uuid.uuid4)
    word: str = Column(String, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False,default=datetime.now)