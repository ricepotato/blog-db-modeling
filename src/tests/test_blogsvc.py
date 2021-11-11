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

        author.last_name = "sukjun"
        author.first_name = "sagong"
        author = self.blog_svc.mod_user(author)
        assert author.last_name == "sukjun"

        author = self.blog_svc.get_user_by_email(email)
        assert author.name == "sukjun"
        new_post = self.blog_svc.add_post("some title", "some article", author)
        assert new_post.author_id == author.id
        new_post = self.blog_svc.add_post("some title 2", "some article 2", author)
        assert new_post.author_id == author.id

        posts = self.blog_svc.get_posts_by_user(author)
        assert len(posts) == 2

        new_category = self.blog_svc.add_category("javascript")
        assert new_category.id

        new_post.category = new_category
        assert self.blog_svc.mod_post(new_post)

        post = self.blog_svc.get_post_by_id(new_post.id)
        assert post.author.name == "sukjun"
        assert post.category.name == "javascript"
