from typing import Any
from typing import Dict

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BOOLEAN
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import func

Base = declarative_base()


class BaseModel(Base):
    """The base model class, which contains the common columns for all models.

    fields:
        * id              primary key
        * create_time     data base create time
        * update_time     data update time
        * is_deleted      data is deleted

    """
    # sqlchemy中, __abstract__设置为True, 这个类可以为基类, 不会被创建为表, 字段能够被子类继承
    __abstract__ = True

    # public fields
    id = Column(Integer, primary_key=True)
    is_deleted = Column(BOOLEAN, default=False)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    update_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def to_dict(self, time_str: bool = False) -> Dict[str, Any]:
        """默认返回全部字段, 子类可以进行重写"""
        return {
            c.name: str(getattr(self, c.name, None)) if time_str and c.name in [
                'create_time',
                'update_time',
            ] else getattr(self, c.name, None)
            for c in self.__table__.columns
        }

    def __repr__(self) -> str:
        """默认打印格式, 子类可以进行重写"""
        return f'<{self.__class__.__name__} {self.id}>'
