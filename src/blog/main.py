import logging
import dotenv
import sys
from service.blog import BlogService


log = logging.getLogger(f"app.{__name__}")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

dotenv.load_dotenv()
bs = BlogService()


def main():
    id = bs.add_author("sukjun.sagong@ahnlab.com", "sukjun")
    author = bs.get_author_by_id(id)
    log.info(f"author 입력 성공 이름:%s, email:%s", author.name, author.email)
    res = bs.mod_author_partial(id, last_name="sagong", first_name="sukjun")
    if res:
        author = bs.get_author_by_id(id)
        log.info(
            f"author %s 변경 성공 first_name:%s, last_name:%s",
            author,
            author.first_name,
            author.last_name,
        )
    else:
        log.error("something wrong!")
        sys.exit(1)

    post_id = bs.add_post("python pip", "제곧내", author)
    new_post = bs.get_post_by_id(post_id)
    log.info(
        f"post 입력 성공 제목:%s, 내용:%s, 작성자:%s, 카테고리:%s, tags:%s",
        new_post.title,
        new_post.article,
        new_post.author,
        new_post.category,
        new_post.tags,
    )
    _ = bs.add_category("python")
    new_category = bs.get_category_by_name("python")
    log.info("category 추가됨. id:%s, name:%s", new_category.id, new_category.name)

    res = bs.mod_post_partial(
        new_post.id, new_category=new_category, new_tags=["python", "javascript"]
    )
    if res:
        updated_post = bs.get_post_by_id(new_post.id)
        log.info("post update 성공. %s", updated_post)
    else:
        log.error("something wrong!")
        sys.exit(1)

    res = bs.mod_post_partial(new_post.id, new_tags=["go", "c++", "python"])
    if res:
        updated_post = bs.get_post_by_id(new_post.id)
        log.info("post update 성공. %s", updated_post)
    else:
        log.error("something wrong!")
        sys.exit(1)

    posts = bs.get_posts_by_author(author)
    log.info("글쓴이 %s", author)
    log.info("posts:")
    for post in posts:
        log.info(post)


if __name__ == "__main__":
    sys.exit(main())
