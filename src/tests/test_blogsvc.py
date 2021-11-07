import unittest
from blog.service.blog import BlogService
from blog.database import Database


class BlotServiceTestCase(unittest.TestCase):
    def tearDown(self):
        pass

    def setUp(self):
        Database().drop_all()
        Database().create_all()
        self.blog_svc = BlogService()

    def test_blog_Svc(self):
        email = "sukjun40@naver.com"
        author = self.blog_svc.add_user(email, "sukjun")
        assert author.id
        author = self.blog_svc.get_author_by_email(email)
        assert author.name == "sukjun"
        new_post = self.blog_svc.add_post("some title", "some article", author)
        assert new_post.author_id == author.id
        new_post = self.blog_svc.add_post("some title 2", "some article 2", author)
        assert new_post.author_id == author.id

        posts = self.blog_svc.get_posts_by_user(author)
        assert posts
