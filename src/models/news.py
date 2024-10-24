from enum import Enum

from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import func
from sqlalchemy import DateTime
from sqlalchemy import Enum as Enum_

from .base_model import BaseModel


class SourceType(Enum):
    BLOOMBERG = 'bloomberg'
    BARRONS = 'barrons'
    UNKNOWN = 'unknown'


class NewsModel(BaseModel):
    __tablename__ = 'news'

    title = Column(String, nullable=False, server_default="", comment='news title')
    content = Column(String, nullable=True, server_default="", comment='news content')
    source = Column(Enum_(SourceType, native_enum=False), nullable=False,server_default=SourceType.UNKNOWN.name, comment='news source')
    article_url = Column(String, nullable=False, server_default="", comment='news url')
    image_url = Column(String, nullable=True, server_default="", comment='news image url')
    day = Column(String(50), nullable=False,server_default="", comment='day of news')
    published_at = Column(DateTime, nullable=False, server_default=func.now(), comment='news published time')
