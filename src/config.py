import typing as t
import yaml
import dacite
from dataclasses import dataclass
import consul
from models.news import SourceType


@dataclass
class CookieStore:
    bloomberg: str
    barron: str


@dataclass
class APIKey:
    worker_ai_key: str


@dataclass
class PromptStore:
    news: str


@dataclass
class ConsulConfig:
    schema: str
    host: str
    token: str
    key: str
    port: t.Optional[int] = 443

    @classmethod
    def from_url(cls, consul_url: str) -> "ConsulConfig":
        """

        :param consul_url: is the fly.io consul url
                example
                    https://:xxx@consul-xxx.fly-shared.net/app-xxx/
        """
        _consul_items = consul_url.split("/")
        consul_items = [i for i in _consul_items if i]

        # schema, host, port, token
        schema = consul_items[0].split(":")[0]
        _token, host = consul_items[1].split("@")
        token = _token.strip(":")

        # parse key value
        # example:
        #    key = app-xxxxx/app
        #

        key_prefix = consul_items[-1]  # key_prefix 是 app-xxxxxxxx
        # app name 是 - 分割的
        app_name_arr = key_prefix.split("-")[:-1]
        app_name = "-".join(app_name_arr)
        key = "/".join([key_prefix, app_name])
        return cls(schema=schema, host=host, token=token, key=key)


@dataclass
class Config:
    # database
    db_url: str
    # web api
    cookie: CookieStore
    origins: t.List[str]
    # ai
    ai_key_store: APIKey
    ai_model: str  # default model
    api_base: str  # api base url for ai
    prompt: PromptStore

    # application
    db_pool_size: t.Optional[int] = 20
    interval: t.Optional[int] = 60 * 5  # interval refresh for spider

    @classmethod
    def from_dict(cls, d: dict):
        return dacite.from_dict(
            cls, d,
        )

    @classmethod
    def from_file(cls, path: str) -> "Config":
        with open(path, 'r') as fp:
            return cls.from_dict(
                yaml.safe_load(fp.read())
            )

    @classmethod
    def from_consul(cls, consol_cfg: ConsulConfig) -> "Config":

        client = consul.Consul(host=consol_cfg.host,
                               port=consol_cfg.port,
                               token=consol_cfg.token,
                               scheme=consol_cfg.schema)

        _, data = client.kv.get(consol_cfg.key)
        if not data:
            raise ValueError("config not found in consul")
        for k, v in data.items():
            if k != "Value":
                continue
            # Valur is bytes
            return cls.from_dict(yaml.safe_load(v))
        raise ValueError("config not found in consul")

    def get_cookie(self, source_type: SourceType) -> str:
        if source_type == SourceType.BLOOMBERG:
            return self.cookie.bloomberg
        elif source_type == SourceType.BARRONS:
            return self.cookie.barron
        else:
            raise ValueError(f"Unknown source type: {source_type}")


def load_cfg(config_path: str) -> Config:
    with open(config_path) as f:
        config_map = yaml.safe_load(f)
        return Config.from_dict(config_map)
