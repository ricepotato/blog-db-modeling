import datetime
import functools
import sqlalchemy
from typing import List
from sqlalchemy.orm import lazyload, joinedload
from sqlalchemy.sql.expression import join
from sqlalchemy.util.langhelpers import decorator
from blog.database.model import BlogAuthor, BlogCategory, BlogPost, BlogTag
from blog.database import Database


class BlogServiceException(Exception):
    pass


class UserNotExist(BlogServiceException):
    pass


class PostNotExist(BlogServiceException):
    pass


def handle_author_not_exist(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlalchemy.orm.exc.NoResultFound as e:
            raise UserNotExist

    return wrapper


def handle_post_not_exist(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlalchemy.orm.exc.NoResultFound as e:
            raise PostNotExist

    return wrapper


class BlogService:
    def __init__(self):
        self.db = Database()

    def add_author(self, email, name, last_name=None, first_name=None) -> int:
        """author 추가
        
        Args:
            email (str): author email
            name (str): author name
            last_name (str): author last_name
            first_name (str): author first_name
        
        Returns:
            author id
            
        Raises:
            SQLAlchemyError: database 오류 발생 시
        """
        with self.db.session_scope() as s:
            new_author = BlogAuthor(
                email=email, name=name, last_name=last_name, first_name=first_name
            )
            s.add(new_author)
        return new_author.id

    @handle_author_not_exist
    def mod_author(self, author: BlogAuthor) -> bool:
        """author 전체 변경
        
        Args:
            author: author to update
        
        Returns:
            True if successfully updated
            
        Raises:
            UserNotExist: author id 가 database 에 없는 경우
        """
        with self.db.session_scope() as s:
            s.add(author)
        return True

    @handle_author_not_exist
    def mod_author_partial(self, author_id: int, **kwargs) -> bool:
        """author 부분 변경
        keyword argument 를 틀리게 입력하면 예외가 발생한다.

        Use:
        >>> BlogService().mod_user_partial(1, last_name="sagong", first_name="sukjun")
        
        Args:
            author_id (int): author id
            kwargs (dict): 변경할 {field: value} dict
        
        Returns:
            True if success
            
        Raises:
            UserNotExist: author id 가 database 에 없는 경우
        """

        with self.db.session_scope() as s:
            obj = s.query(BlogAuthor).filter(BlogAuthor.id == author_id).one()
            for k, v in kwargs.items():
                setattr(obj, k, v)
            s.add(obj)
        return True

    @handle_author_not_exist
    def get_author_by_email(self, email: str) -> BlogAuthor:
        """이메일로 author 검색

        Args:
            email (str): author email
        
        Returns:
            author or None
        """
        with self.db.session_scope() as s:
            return s.query(BlogAuthor).filter(BlogAuthor.email == email).one_or_none()

    @handle_author_not_exist
    def get_author_by_id(self, id: int) -> BlogAuthor:
        """author id 로 검색
        
        Args:
            id (int): author id
        
        Returns:
            author
            
        Raises:
            UserNotExist: author id 가 database 에 없는 경우
        """

        with self.db.session_scope() as s:
            return s.query(BlogAuthor).filter(BlogAuthor.id == id).one()

    def add_post(
        self,
        title: str,
        article: str,
        author: BlogAuthor,
        category: BlogCategory = None,
        tags: List[str] = None,
    ) -> int:
        """blog post 추가
        이미 저장된 category 가 있으면 해당 category 내로 추가
        tags str list 입력받고 BlogTag 데이터가 있으면 지정, 없으면 입력후 저장

        BlogAuthor 객체를 을 만들어야 해서 귀찮다. 😅
        BlogAuthor 객체가 Session 에 박혀있는 경우도 있다.

        BlogCategory 는 검색해서 만든다.
        
        Args:
            title (str): blog post title
            article (str): blog post article
            author (BlogAuthor): 글쓴이
            category (BlogCategory): 블로그 카테고리
            tags (List[str]): 블로그 글 tags
        
        Returns:
            author
            
        """
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
        return new_post.id

    @handle_post_not_exist
    def mod_post(
        self,
        post_id: int,
        title: str,
        article: str,
        category: BlogCategory = None,
        tags: List[str] = None,
    ) -> bool:
        with self.db.session_scope() as s:

            post = s.query(BlogPost).filter(BlogPost.id == post_id).one()
            post.title = title
            post.article = article
            post.category = category
            if tags is not None:
                for tag_name in tags:
                    blog_tag = s.query(BlogTag).filter(
                        BlogTag.name == tag_name
                    ).first() or BlogTag(name=tag_name)
                    post.tags.append(blog_tag)

            s.add(post)
        return True

    @handle_post_not_exist
    def get_post_by_id(self, post_id: int) -> BlogPost:
        with self.db.session_scope() as s:
            post = (
                s.query(BlogPost)
                .filter(BlogPost.id == post_id)
                .options(
                    joinedload(BlogPost.author),
                    joinedload(BlogPost.category),
                    joinedload(BlogPost.tags),
                )
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

    def add_category(self, name: str) -> int:
        with self.db.session_scope() as s:
            new_category = BlogCategory(name=name)
            s.add(new_category)
        return new_category.id

    def get_category_by_name(self, name: str) -> BlogCategory:
        with self.db.session_scope() as s:
            return s.query(BlogCategory).filter(BlogCategory.name == name).one_or_none()

    def get_posts_by_category_name(self, name: str) -> List[BlogPost]:
        with self.db.session_scope() as s:
            category = s.query(BlogCategory).filter(BlogCategory.name == name).one()
            return category.posts

    def get_posts_by_author(
        self, author: BlogAuthor, limit=5, offset=0
    ) -> List[BlogPost]:
        with self.db.session_scope() as s:
            obj = s.query(BlogAuthor).filter(BlogAuthor.id == author.id).one()
            return obj.posts.order_by(BlogPost.id.desc())[offset : limit + offset]

    def get_tags(self) -> List[BlogTag]:
        with self.db.session_scope() as s:
            return s.query(BlogTag).all()

