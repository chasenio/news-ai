import logging
import yaml
import os
from typing import TYPE_CHECKING
from logging import Filter
from typing import Optional
from logging.config import dictConfig

if TYPE_CHECKING:
    from logging import LogRecord

from apps.middleware.connecting import connection_ctx
from apps.middleware.connecting import took
from apps.middleware.connecting import ClientInfo

_logger = logging.getLogger(__name__)

LOGGING_FILE = "logging.yml"


def load_logging_cfg(path: Optional[str] = LOGGING_FILE, default_level: Optional[str] = 'INFO', env_key='LOG_CFG'):
    """Load logging configuration from a YAML file.
    """
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        print("Loading logging configuration from {}".format(path))
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        dictConfig(config)
        return config
    else:
        _logger.info("Logging configuration file not found at %s", path)
        logging.basicConfig(level=default_level)


class ConnectFilter(Filter):

    """在日志中添加IP"""
    def __init__(self, name: str = '', default_value: Optional[str] = None):
        super().__init__(name=name)
        self.default_value = default_value

    def filter(self, record: 'LogRecord'):
        connecting_ip = connection_ctx.get(ClientInfo(self.default_value))
        record.connect_ip = format_client(connecting_ip)
        return True


class TookFilter(Filter):
    """在日志中添加请求耗时"""
    def __init__(self, name: str = '', default_value: Optional[float] = None):
        super().__init__(name=name)
        self.default_value = default_value

    def filter(self, record: 'LogRecord'):
        request_took = took.get(self.default_value)
        if request_took:
            record.took = f"{request_took * 1000:.3f}ms"
        else:
            record.took = ""
        return True


def format_client(client: ClientInfo) -> str:
    if client.port != 0:
        return f"{client.ip}:{client.port}"
    if client.country:
        return f"{client.ip}:{client.country}"
    return client.ip