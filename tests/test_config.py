import pytest
import logging
from config import Config
from config import ConsulConfig

_logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "consul_url", (
            "https://:xx@consul-syd-5.fly-shared.net/news-ai-xxx/",
    )
)
def test_config_consul(consul_url: str):
    print(consul_url.split("/"))
    schema = consul_url.split("/")[0].split(":")[0]
    _token, host = consul_url.split("/")[2].split("@")
    token = _token.strip(":")

    print(schema)
    print(host)
    print(token)
    consul_cfg = ConsulConfig.from_url(consul_url)
    cfg = Config.from_consul(consul_cfg)
    print(cfg)
