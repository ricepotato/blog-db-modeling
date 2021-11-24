import unittest
from blog.service.blog import BlogService, CategoryNotExist, AuthorNotExist
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
        id = self.blog_svc.add_author(email, "ricepotato")
        assert id != 0

        res = self.blog_svc.get_author_by_email("1234")
        assert res is None

        with self.assertRaises(AuthorNotExist):
            _ = self.blog_svc.get_author_by_id(0)

        res = self.blog_svc.mod_author_partial(
            id, last_name="sagong", first_name="sukjun"
        )
        assert res

        author = self.blog_svc.get_author_by_id(id)
        assert author.last_name == "sagong"
        assert author.first_name == "sukjun"

        # 오타가 발생할 수 있음
        res = self.blog_svc.mod_author_partial(
            id, list_name="sagong", first_name="sukjun"
        )
        assert res

        author.first_name = "hello"
        author.last_name = "world"

        # author 전체 업데이트
        res = self.blog_svc.mod_author(author)
        assert res
        updated_author = self.blog_svc.get_author_by_id(author.id)
        assert updated_author.first_name == "hello"
        assert updated_author.last_name == "world"

        id = self.blog_svc.add_category("javascript")
        assert id != 0
        id = self.blog_svc.add_category("python")
        assert id != 0

        author = self.blog_svc.get_author_by_email(email)
        id = self.blog_svc.add_post(
            "this is post title", "this is post without category", author
        )
        assert id != 0

        with self.assertRaises(CategoryNotExist):
            category = self.blog_svc.get_category_by_name("c++")

        category = self.blog_svc.get_category_by_name("javascript")
        id = self.blog_svc.add_post(
            "this is post title",
            "this is post with category and tags",
            author,
            category,
            ["javascript", "python"],
        )
        assert id

        post = self.blog_svc.get_post_by_id(id)
        assert post
        assert post.author.name
        assert post.category
        assert post.tags

        new_tags = ["c++", "go", "javascript"]
        res = self.blog_svc.mod_post_partial(post.id, new_tags=new_tags)
        assert res

        post = self.blog_svc.get_post_by_id(post.id)
        assert post.tags
        tag_names = [tag.name for tag in post.tags]
        # new tags 에 전부 포함되어있는지 확인
        for tag_name in tag_names:
            assert tag_name in new_tags

        id = self.blog_svc.add_author("sukjun.sagong@ahnlab.com", "sukjun.sagong")
        assert id != 0
        author2 = self.blog_svc.get_author_by_id(id)

        js_category = self.blog_svc.get_category_by_name("javascript")
        for idx in range(40):
            id = self.blog_svc.add_post(
                f"this is post title {idx}",
                "this is post without category {idx}",
                author2,
                js_category,
            )
            assert id != 0

        posts = self.blog_svc.get_posts_by_author(author2, limit=3, offset=0)
        assert len(posts) == 3
        assert posts[0].id == 42
        assert posts[1].id == 41
        assert posts[2].id == 40
        posts = self.blog_svc.get_posts_by_author(author2, limit=3, offset=3)
        assert len(posts) == 3
        assert posts[0].id == 39
        assert posts[1].id == 38
        assert posts[2].id == 37

        posts = self.blog_svc.get_posts_by_category_name("javascript")
        assert len(posts) == 5
