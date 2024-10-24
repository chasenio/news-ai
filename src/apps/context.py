from contextvars import ContextVar, Token
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

class ContextWrapper(Generic[T]):
    def __init__(self, value: ContextVar[T]):
        self.__value: ContextVar[T] = value

    def set(self, value: T) -> Token[T]:
        return self.__value.set(value)

    def reset(self, token: Token[T]) -> None:
        self.__value.reset(token)

    @property
    def value(self) -> T:
        return self.__value.get()


db_ctx = ContextWrapper[AsyncSession](ContextVar("db", default=None))
config_ctx = ContextWrapper[dict](ContextVar("config", default=None))