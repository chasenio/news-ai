import pytest
import logging

from services.news.data import Page
from services.news.service import NewsService

_logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "model, prompt", (
        ["@cf/meta/llama-2-7b-chat-fp16", "你是资深金融交易员,请你根据用户输入的多条经济新闻, 精简总结. 按照国家/人物/公司 进行分类输出."],
    )
)
def test_ai_summary(news_service: NewsService, model: str, prompt: str):

    news = news_service.find(page=Page(limit=10))

    input: str =  ""

    for i, new in enumerate(news):
        input += f"{i+1}. {new.title} {new.published_at.isoformat()}\n"

    response =  news_service.chat_call(prompt=prompt,content=input, model=model)
    for s in response:
        if s:
            print(f"{s}", end="")

