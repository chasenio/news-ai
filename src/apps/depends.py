from fastapi import Depends

from services.news.service import NewsService

from .context import db_ctx
from .context import config_ctx



class GetNewSvc:

    def __call__(self):
        return NewsService(
            db=db_ctx.value,
            cfg=config_ctx.value
        )


get_news_svc = GetNewSvc()

