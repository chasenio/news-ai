import os
import asyncio
import functools
from typing import Optional
from starlette.middleware.cors import CORSMiddleware

import click
from fastapi import FastAPI
from uvicorn import Server
from uvicorn import Config as UvicornConfig

from models.helpers import upgrade_db
from models.session import DBConnect

from apps import router
from apps.context import db_ctx
from apps.context import config_ctx
from apps.middleware.connecting import ConnectMiddleware
from config import Config
from config import ConsulConfig

from services.task.news_loop import NewsLoop
from services.news.service import NewsService

from utils.logger import load_logging_cfg

ENV_CONSUL_KEY = 'FLY_CONSUL_URL'


class NewsApp(Server):
    pass


def make_app(config: Config) -> FastAPI:
    app = FastAPI()

    app.add_middleware(ConnectMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    @app.get("/health",
             name='health',
             tags=['Ping'])
    def health():
        return {'status': 'ok'}

    return app


def make_sync(func):
    """"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


@click.command()
@make_sync
@click.option('--config', '-c', type=str, help='config file path')
async def main(config: Optional[str]):
    log_cfg = load_logging_cfg()
    # load config
    if config:
        cfg = Config.from_file(config)
    elif consul_url := os.getenv(ENV_CONSUL_KEY):
        consul_cfg = ConsulConfig.from_url(consul_url)
        cfg = Config.from_consul(consul_cfg)
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

    # start spider
    news_svc = NewsService(db=_db, cfg=cfg)
    news_loop = NewsLoop(news_svc=news_svc, config=cfg)
    news_loop.start()

    # create web api
    app = make_app(config=cfg)
    serve = NewsApp(config=UvicornConfig(app=app, host="0.0.0.0", log_config=log_cfg))

    api = asyncio.create_task(serve.serve())

    await asyncio.gather(api)


if __name__ == '__main__':
    main()
