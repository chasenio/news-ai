import logging
import typing as t
from datetime import date
from datetime import datetime

from sqlalchemy.orm import Session
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate

from models.session import DBConnect

from models.news import SourceType
from models.news import NewsModel
from .data import New
from .data import Page

from config import Config

_logger = logging.getLogger(__name__)


class NewsService:
    def __init__(self, db: DBConnect, cfg: Config):
        self.db = db
        self.cfg = cfg
        self.llm = ChatOpenAI(
            streaming=True,
            openai_api_base=self.cfg.api_base,
            api_key=self.cfg.ai_key_store.worker_ai_key,
            model=self.cfg.ai_model,
            timeout=200,
            max_retries=2,
            temperature=0.4,
        )


    def chat_call(self, prompt: str, content: str, model: t.Optional[str] = None):

        message = [
            SystemMessage(
                content=prompt
            ),
            HumanMessage(
                content=content
            )
        ]
        try:
            if model:
                self.llm.model_name = model
            parser = StrOutputParser()
            chain = self.llm | parser
            # response = self.llm.stream(message) # 结构化数据
            response = chain.stream(message) # 仅 content 流式数据
        except Exception as e:
            _logger.info(f"e: {e}")
            raise
        return response

    def find(self,
             day: t.Optional[date] = None,
             title: str = None,
             source_type: t.Optional[SourceType] = None,
             page: t.Optional[Page] = Page(),
             begin: t.Optional[datetime] = 0,
             ) -> t.Iterator[NewsModel]:
        with self.db.session() as session:
            query = session.query(NewsModel).order_by(NewsModel.published_at.desc())
            if day:
                query = query.filter(NewsModel.day == f"{day:%Y/%m/%d}")
            if title:
                title_like = f"%{title}%"
                query = query.filter(NewsModel.title.ilike(title_like))  # ilike 不区分大小写
            if source_type:
                query = query.filter(NewsModel.source == source_type)
            if begin:
                query = query.filter(NewsModel.published_at >= begin)
            if page:
                query = query.limit(page.limit).offset((page.page - 1) * page.limit)
            return query.all()

    def add(self, news: t.List[New], session: Session):
        instances = [
            NewsModel(
                title=i.title.strip(),
                source=i.source_type,
                article_url=i.article_url,
                image_url=i.image_url,
                content=i.content,
                day=i.published_at.strftime('%Y/%m/%d'),
                published_at=i.published_at
            ) for i in news
        ]
        session.add_all(instances)

    def is_exist(self, title: str, session: Session) -> bool:
        return session.query(NewsModel).filter(NewsModel.title == title).first()

    def list_days(self, session: Session) -> t.List[str]:
        result = []
        for day in session.query(NewsModel.day).distinct():
            result.append(day[0])
        return result
