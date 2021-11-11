import datetime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql.schema import MetaData, Table
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


Base: Table = declarative_base()


class TimeStampedMixin(object):
    @declared_attr
    def created_at(cls):
        return sqlalchemy.Column(DateTime, default=datetime.datetime.utcnow)

    @declared_attr
    def updated_at(cls):
        return sqlalchemy.Column(DateTime, default=datetime.datetime.utcnow)


class BlogAuthor(Base, TimeStampedMixin):
    __tablename__ = "blog_author"
    id = Column(Integer, primary_key=True)
    email = Column(String(45), unique=True)
    name = Column(String(45))
    first_name = Column(String(45))
    last_name = Column(String(45))

    posts = relationship("BlogPost")


class BlogPost(Base, TimeStampedMixin):
    __tablename__ = "blog_post"
    id = Column(Integer, primary_key=True)
    title = Column(String(144))
    article = Column(String)
    date_published = Column(DateTime)
    views = Column(Integer)
    author_id = Column(Integer, ForeignKey("blog_author.id"))
    category_id = Column(Integer, ForeignKey("blog_category.id"), nullable=True)

    author = relationship("BlogAuthor")
    category = relationship("BlogCategory")


class BlogCategory(Base, TimeStampedMixin):
    __tablename__ = "blog_category"
    id = Column(Integer, primary_key=True)
    name = Column(String(20))

    posts = relationship("BlogPost")
