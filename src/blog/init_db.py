import dotenv
from service.blog import BlogService

dotenv.load_dotenv()
bs = BlogService()
bs.db.drop_all()
bs.db.create_all()
