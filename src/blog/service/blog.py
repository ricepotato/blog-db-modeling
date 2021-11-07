import datetime
from typing import List
from sqlalchemy.orm.session import Session
from blog.database.model import BlogAuthor, BlogPost
from blog.database import Database


class BlogService:
    def __init__(self):
        self.db = Database()

    def add_user(self, email, name, last_name=None, first_name=None) -> BlogAuthor:
        with self.db.session_scope() as s:
            new_author = BlogAuthor(
                email=email, name=name, last_name=last_name, first_name=first_name
            )
            s.add(new_author)
            s.commit()
            return new_author.id

    def get_user_by_email(self, email: str) -> BlogAuthor:
        with self.db.session_scope() as s:
            author = s.query(BlogAuthor).filter(BlogAuthor.email == email).one()
            s.expunge_all()
            return author

    def add_post(self, title: str, article: str, author: BlogAuthor) -> BlogPost:
        with self.db.session_scope() as s:
            now = datetime.datetime.utcnow()
            new_post = BlogPost(
                title=title, article=article, date_published=now, views=0, author=author
            )
            s.add(new_post)
            s.flush()
            s.expunge(new_post)
            return new_post

    def get_posts_by_user(self, author: BlogAuthor) -> List[BlogPost]:
        pass
