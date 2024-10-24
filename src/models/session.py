from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

from psycopg2.extensions import ISOLATION_LEVEL_REPEATABLE_READ

class DBConnect:
    def __init__(self, db_url, **kwargs):
        self.conn = create_engine(db_url, **kwargs)
        self.conn.connect().connection.set_isolation_level(ISOLATION_LEVEL_REPEATABLE_READ)
        self.sessionmaker = sessionmaker(bind=self.conn, expire_on_commit=False)

    @contextmanager
    def session(self, **kwargs) -> Session:
        session = self.sessionmaker(**kwargs)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @classmethod
    def make_conn(cls, db_url, **kwargs):
        return cls(db_url, **kwargs)
