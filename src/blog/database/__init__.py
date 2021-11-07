import logging
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from .model import Base


log = logging.getLogger(f"app.{__name__}")

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"


class Singleton(type):
    """Singleton.
    @see: http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(object):

    __metaclass__ = Singleton

    def __init__(self):

        self.engine = create_engine(
            SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )
        self.Session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False
        )

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            log.error("Database Error. %s", e)
            session.rollback()
            raise
        finally:
            session.close()

    def create_all(self):
        """creates all tables."""
        try:
            Base.metadata.create_all(self.engine)
        except SQLAlchemyError as e:
            log.error("Unable to create or connect to database: %s", e)
            raise

    def drop_all(self):
        """Drop all tables."""
        try:
            Base.metadata.drop_all(self.engine)
        except SQLAlchemyError as e:
            log.error("Unable to drop all tables of the database: %s", e)
            raise
