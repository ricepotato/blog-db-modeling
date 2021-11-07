from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import MetaData, Table
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

Base: Table = declarative_base()


class BlogAuthor(Base):
    __tablename__ = "blog_author"
    id = Column(Integer, primary_key=True)
    email = Column(String(45), unique=True)
    name = Column(String(45))
    first_name = Column(String(45))
    last_name = Column(String(45))

    posts = relationship("BlogPost", backref="author")


class BlogPost(Base):
    __tablename__ = "blog_post"
    id = Column(Integer, primary_key=True)
    title = Column(String(144))
    article = Column(String)
    date_published = Column(DateTime)
    views = Column(Integer)
    author_id = Column(Integer, ForeignKey("blog_author.id"))

    # author = relationship("BlogAuthor", back_populates="posts")
