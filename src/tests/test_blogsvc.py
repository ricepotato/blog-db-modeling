import unittest
from blog.service.blog import BlogService
from blog.database.model import Base
from blog.database import Database


class BlotServiceTestCase(unittest.TestCase):
    def tearDown(self):
        pass

    def setUp(self):
        Database().drop_all()
        Database().create_all()
        # Base.metadata.drop_all(bind=engine)
        # Base.metadata.create_all(bind=engine)
        self.blog_svc = BlogService()

    def test_blog_Svc(self):
        email = "sukjun40@naver.com"
        id = self.blog_svc.add_user(email, "sukjun")
        assert id
        # user = self.blog_svc.get_user_by_email(email)
        # assert user.name == "sukjun"
        # post = self.blog_svc.add_post("some title", "some article", user)
        # assert post.author_id
        # assert post.author
        # post = self.blog_svc.add_post("some title 2", "some article 2", user)
        # assert post.author_id
        # assert post.author

        # posts = self.blog_svc.get_posts_by_user(user)
