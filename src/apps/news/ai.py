import typing as t
from fastapi import Depends
from fastapi import APIRouter
from datetime import timedelta
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

from config import Config
from services.news.service import NewsService
from ..depends import get_news_svc
from ..context import config_ctx
from utils.time import datetime_utc

router = APIRouter()


class NewsAIRequest(BaseModel):
    prompt: t.Optional[str] = None
    begin: t.Optional[int] = 24  # default 24 hours


@router.post("/ai")
async def news_ai(req: t.Optional[NewsAIRequest] = NewsAIRequest(), news_svc: NewsService = Depends(get_news_svc)):
    # make prompt
    config: Config = config_ctx.value
    prompt = req.prompt if req and req.prompt else config.prompt.news

    begin = datetime_utc() - timedelta(hours=req.begin)
    # make input context
    news = news_svc.find(begin=begin)
    input: str = ""
    for i, new in enumerate(news):
        input += f"{i + 1}. {new.title} source:{new.source} {new.published_at.isoformat()}\n"

    # call ai
    stream = news_svc.chat_call(prompt=prompt, content=input, model=config.ai_model)

    # output stream
    def generator():
        for chunk in stream:
            yield chunk

    response_stream = generator()
    return StreamingResponse(response_stream, media_type="text/event-stream")
