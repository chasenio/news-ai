import os
import click
from typing import Optional

from models.helpers import upgrade_db
from models.session import DBConnect

from apps.context import db_ctx
from apps.context import config_ctx
from config import Config

from services.news.service import NewsService

from utils.logger import load_logging_cfg

ENV_CONSUL_KEY = 'FLY_CONSUL_URL'

load_logging_cfg()


@click.command()
@click.option('--config', '-c', type=str, help='config file path')
def main(config: Optional[str]):
    # load config
    if config:
        cfg = Config.from_file(config)
    elif os.getenv(ENV_CONSUL_KEY):
        cfg = Config.from_consul(os.getenv(ENV_CONSUL_KEY))
    else:
        raise ValueError('config not found')

    # db migration
    alembic_path = os.path.join(os.path.dirname(__file__), 'alembic.ini')
    upgrade_db(cfg.db_url, alembic_path)

    _db = DBConnect(db_url=cfg.db_url, echo=False, pool_size=cfg.db_pool_size, pool_recycle=600,
                    pool_pre_ping=True,
                    pool_use_lifo=True, future=True)
    db_ctx.set(_db)
    config_ctx.set(cfg)

    news_svc = NewsService(db=_db, cfg=cfg)

    # test
    news = news_svc.find()
    input: str = ""

    for i, new in enumerate(news):
        input += f"{i + 1}. {new.title} {new.published_at.isoformat()}\n"

    response = news_svc.chat_call(prompt=cfg.prompt.news, content=input, )
    for s in response:
        if s:
            print(f"{s}", end="")


if __name__ == '__main__':
    main()
