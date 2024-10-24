import pytest
import logging
from services.news.service import NewsService


_logger = logging.getLogger(__name__)

def test_find(news_service: NewsService ):

    result = news_service.find(title="US")
    _logger.info(f"{result}")
