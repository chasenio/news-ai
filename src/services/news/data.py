import typing as t

from dataclasses import dataclass
from models.news import SourceType
from datetime import datetime


@dataclass
class New:
    title: str
    source_type: SourceType
    article_url: str
    image_url: t.Optional[str] = None
    content: t.Optional[str] = None
    published_at: t.Optional[datetime] = None


@dataclass
class Page:
    page: t.Optional[int] = 1
    limit: t.Optional[int] = 20
