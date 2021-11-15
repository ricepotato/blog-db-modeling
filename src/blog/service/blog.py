import datetime
from typing import List

from sqlalchemy.orm import lazyload, joinedload
from blog.database.model import BlogAuthor, BlogCategory, BlogPost, BlogTag
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
        return new_author

    def mod_user(self, author: BlogAuthor) -> bool:
        with self.db.session_scope() as s:
            s.add(author)
        return author

    def get_user_by_email(self, email: str) -> BlogAuthor:
        with self.db.session_scope() as s:
            return s.query(BlogAuthor).filter(BlogAuthor.email == email).one_or_none()

    def add_post(
        self,
        title: str,
        article: str,
        author: BlogAuthor,
        category: BlogCategory = None,
        tags: List[str] = None,
    ) -> BlogPost:
        with self.db.session_scope() as s:
            new_post = BlogPost(title=title, article=article, author=author)

            if category is not None:
                new_post.category = category

            if tags is not None:
                for tag_name in tags:
                    blog_tag = s.query(BlogTag).filter(
                        BlogTag.name == tag_name
                    ).first() or BlogTag(name=tag_name)
                    new_post.tags.append(blog_tag)
            s.add(new_post)
        return new_post

    def mod_post(self, post: BlogPost) -> bool:
        with self.db.session_scope() as s:
            s.add(post)
        return True

    def get_post_by_id(self, post_id: int) -> BlogPost:
        with self.db.session_scope() as s:
            post = (
                s.query(BlogPost)
                .filter(BlogPost.id == post_id)
                .options(joinedload(BlogPost.author), joinedload(BlogPost.category))
                .one()
            )
            return post

    def get_posts_by_user(self, author: BlogAuthor) -> List[BlogPost]:
        with self.db.session_scope() as s:
            return (
                s.query(BlogPost)
                .filter(BlogPost.author == author)
                .order_by(BlogPost.id.desc())
                .all()
            )

    def add_category(self, name: str) -> BlogCategory:
        with self.db.session_scope() as s:
            new_category = BlogCategory(name=name)
            s.add(new_category)
        return new_category

    def get_posts_by_category_name(self, name: str) -> List[BlogPost]:
        with self.db.session_scope() as s:
            category = s.query(BlogCategory).filter(BlogCategory.name == name).one()
            return category.posts

    def get_tags(self) -> List[BlogTag]:
        with self.db.session_scope() as s:
            return s.query(BlogTag).all()
