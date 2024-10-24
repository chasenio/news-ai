import typing as t
import httpx
from threading import Thread
import logging
from threading import Condition
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

from config import Config
from models.session import DBConnect
from models.news import SourceType
from services.news.parse import parse_news
from dataclasses import dataclass
from ..news.service import NewsService

_logger = logging.getLogger(__name__)


@dataclass
class NewsTask:
    url: str
    source_type: SourceType


def capture_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            _logger.exception(f"process err:")

    return inner


class NewsLoop:

    def __init__(self, news_svc: NewsService, config: Config, pool: t.Optional[ThreadPoolExecutor] = None,
                 pool_size: int = 4):
        self.new_svc = news_svc
        self._cond = Condition()
        self.pool = pool
        self.config = config
        self.client = httpx.Client(headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "Cache-Control": "max-age=0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip",
            "Accept-Language": "en-Us,en;q=0.9,en;q=0.8",
            "DNT": "1",
        })

        if not self.pool:
            self.pool = ThreadPoolExecutor(max_workers=pool_size)

    def start(self):
        t = Thread(target=self.run)
        _logger.info(f"news loop start")
        t.start()

    def stop(self):
        with self._cond:
            self._cond.notify_all()

    def run(self):
        _logger.info("news loop run")

        tasks: t.List[NewsTask] = [
            NewsTask("https://www.bloomberg.com/latest", SourceType.BLOOMBERG),
            NewsTask("https://www.barrons.com/real-time/", SourceType.BARRONS),
        ]

        while True:

            for i in tasks:
                self.pool.submit(self.process_task, i)

            with self._cond:
                self._cond.wait(self.config.interval)

    @capture_error
    def process_task(self, task: NewsTask):
        """
        1. get html form url
        2. parse html to news
        3. is news exist
        4. save news
        """
        cookie = {i.split("=")[0]: i.split("=")[1] for i in self.config.get_cookie(task.source_type).split(";")}

        response = self.client.get(task.url, cookies=cookie)
        response.encoding = "utf-8"

        with self.new_svc.db.session() as sess:

            _pending_news = []

            # parse html to news
            for i in parse_news(response.content.decode("utf-8"), task.source_type):
                _logger.info(f"news: {i.title}")
                if self.new_svc.is_exist(i.title.strip(), session=sess):
                    _logger.info(f"news: {i.title} is already.")
                    continue
                _pending_news.append(i)

            _logger.info(f"pending news: {len(_pending_news)}")
            # save news
            self.new_svc.add(_pending_news, session=sess)
        _logger.info(f"task: {task.url} done, news: {len(_pending_news)}")
