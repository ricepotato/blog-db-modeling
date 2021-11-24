import os
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
        connection_string = self._get_connection_string()
        ECHO_SQL = bool(
            os.environ.get("ECHO_SQL", "false").lower() in ["1", "true", "yes"]
        )
        self.engine = create_engine(
            connection_string, connect_args={"check_same_thread": False}, echo=ECHO_SQL,
        )
        self.Session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False
        )

    def _get_connection_string(self):
        dbms = os.environ.get("DBMS", "sqlite")
        if dbms == "sqlite":
            return SQLALCHEMY_DATABASE_URL
        elif dbms == "mysql":
            db_name = os.environ.get("MYSQL_DATABASE")
            user_name = os.environ.get("MYSQL_USERNAME")
            password = os.environ.get("MYSQL_PASSWORD")
            mysql_host = os.environ.get("MYSQL_HOST")
            return f"mysql+pymysql://{user_name}:{password}@{mysql_host}/{db_name}?charset=utf8mb4"
        else:
            raise ValueError

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
