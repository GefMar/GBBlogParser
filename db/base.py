from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


class BlogPostDataBase:

    def __init__(self, base, table_post, table_creator, table_tags, data_base_info):
        self.table_post = table_post
        self.table_creator = table_creator
        self.table_tags = table_tags
        self.base = base
        self.database_path = \
            f'''{
            data_base_info["type"]
            }://{
            data_base_info["user"]
            }:{
            data_base_info["pass"]
            }@{
            data_base_info["url"]
            }/{
            data_base_info["name"]
            }'''

    def get_session(self):

        engine = create_engine(self.database_path)

        if not database_exists(engine.url):
            create_database(engine.url)

        self.base.metadata.create_all(engine)
        db_session = sessionmaker(bind=engine)
        db_session.configure(bind=engine)
        session = db_session()
        return session

    def set_post(self, session, **kwargs):
        url = kwargs.get('url')
        title = kwargs.get('title')
        post_img = kwargs.get('post_img')
        image_path = kwargs.get('image_path')
        description = kwargs.get('description')
        date = kwargs.get('date')
        text = kwargs.get('text')
        post_creator = kwargs.get('post_creator')
        post_tags = kwargs.get('tags')
        blog_post = self.table_post(url, title, post_img, image_path, description, date, text, post_creator, post_tags)
        session.add(blog_post)
        return blog_post

    def set_creator(self, session, **kwargs):
        creator_temp = self.table_creator(url=kwargs.get('url'), name=kwargs.get('name'))
        creator = self.__create_of_update(session, self.table_creator, creator_temp.url, creator_temp)
        return creator

    def set_tags(self, session, *args):
        tags = []
        for item in args:
            tag_temp = self.table_tags(url=item.get('url'), name=item.get('name'))
            tag = self.__create_of_update(session, self.table_tags, tag_temp.url, tag_temp)
            tags.append(tag)
        return tags

    def __create_of_update(self, session, table, uniq, strict_obj):
        result = session.query(table).filter(table.url == uniq).first()
        if not result:
            session.add(strict_obj)
            return strict_obj
        return result
