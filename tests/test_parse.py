import logging

import pytest

from datetime import date

from services.news.parse import parse_news
from services.news.service import NewsService
from models.news import SourceType
from models.session import DBConnect

_logger = logging.getLogger(__name__)


@pytest.mark.parametrize("path, source_type", (
        ("", SourceType.BLOOMBERG),
        ("", SourceType.BARRONS),
))
def test_parse_html(path: str, source_type: SourceType, news_service: NewsService, db: DBConnect):

    with open(path, "r") as f:

        with db.session() as session:

            result = []
            for i in parse_news(f.read(), source_type):
                if news_service.is_exist(title=i.title, session=session):
                    _logger.warning(f"i: {i} is already.")
                    continue
                result.append(i)

            news_service.add(result, session=session)




def test_days(news_service: NewsService, db: DBConnect):
    with db.session() as session:
        days = news_service.list_days(session=session)
        _logger.info(f"days: {days}")
        assert days


@pytest.mark.parametrize(
    "day",
    (
        "2024-10-12",
    )
)
def test_news_find(news_service: NewsService, day: str):

    d = date.fromisoformat(day)
    news = news_service.find(day=d)
    _logger.info(f"news: {news}")
    assert news