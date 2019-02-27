from db.models import Base, BlogPost, Creator, Tags
from db.base import BlogPostDataBase
from config import DATA_BASE

database = BlogPostDataBase(base=Base,
                            table_post=BlogPost,
                            table_creator=Creator,
                            table_tags=Tags,
                            data_base_info=DATA_BASE)
