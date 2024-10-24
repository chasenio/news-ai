import logging
from alembic import command
from alembic.config import Config as AlembicConfig

from sqlalchemy_utils import database_exists, create_database

_logger = logging.getLogger(__name__)


# upgrade database schema and data
def upgrade_db(db_url: str, alembic_cfg_file: str):
    _logger.info('ensure database schema from {}'.format(alembic_cfg_file))

    create_database_by_url(db_url)

    alembic_cfg = AlembicConfig(alembic_cfg_file)
    if db_url:
        _logger.info('overriding sqlachemy.url')
        alembic_cfg.set_main_option('sqlalchemy.url', db_url)
    command.upgrade(alembic_cfg, "head")


def create_database_by_url(db_url: str):
    _logger.info('call create database')

    if not database_exists(db_url):
        _logger.info("Creating database...")
        create_database(db_url)
        _logger.info("Database created successfully")
