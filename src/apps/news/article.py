from typing import Optional

from fastapi import Depends
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import timezone

from ..depends import get_news_svc
from services.news.data import Page
from services.news.service import NewsService
from models.news import SourceType

r = APIRouter()


class DaysResponse(BaseModel):
    days: list[str]


@r.get("/days")
def days(news_svc: NewsService = Depends(get_news_svc)) -> DaysResponse:
    """聚合新闻日期"""
    with news_svc.db.session() as session:
        return DaysResponse(days=news_svc.list_days(session=session))


class Article(BaseModel):
    article_id: int
    title: str
    source: str
    published_at: str
    image_url: str
    url: str


class NewsResponse(BaseModel):
    articles: list[Article]


class SearchRequest(BaseModel):
    source: str = None
    query: str = None


@r.post("/search", response_model=NewsResponse)
def search(req: SearchRequest, news_service: NewsService = Depends(get_news_svc)) -> NewsResponse:
    """通过标题搜索新闻"""
    news = news_service.find(
        title=req.query,
    )
    return NewsResponse(
        articles=[
            Article(
                article_id=i.id,
                title=i.title,
                source=i.source,
                published_at=i.published_at.isoformat(),
                image_url=i.image_url,
                url=i.article_url
            ) for i in news
        ]
    )


@r.get("/articles", response_model=NewsResponse)
def articles(p: int = 1, limit: int = 5, title: Optional[str] = None, source: Optional[SourceType] = None,
             news_service: NewsService = Depends(get_news_svc)) -> NewsResponse:
    """
    查看新闻
    """
    news = news_service.find(page=Page(page=p, limit=limit, ), title=title, source_type=source)
    return NewsResponse(
        articles=[
            Article(
                article_id=i.id,
                title=i.title,
                source=i.source.name,
                published_at=i.published_at.replace(tzinfo=timezone.utc).isoformat(),
                image_url=i.image_url,
                url=i.article_url
            ) for i in news
        ]
    )
