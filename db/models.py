
from sqlalchemy import Table, Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

association_tag_table = Table('association_tags', Base.metadata,
                              Column('blog_post', Integer, ForeignKey('blog_post.id')),
                              Column('tags', Integer, ForeignKey('tags.id'))
                              )


class BlogPost(Base):
    __tablename__ = 'blog_post'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    url = Column(String, unique=True)
    title = Column(String)
    post_img = Column(String)
    image_path = Column(String)
    description = Column(String)
    date = Column(String)
    text = Column(String)
    post_creator = Column(Integer, ForeignKey('creator.id'))
    creator = relationship('Creator', backref='creator')
    post_tags = relationship('Tags', secondary=association_tag_table, backref='posts')

    def __init__(self, url, title, post_img, image_path, description, date, text, post_creator, post_tags):
        self.url = url
        self.title = title
        self.post_img = post_img
        self.image_path = image_path
        self.description = description
        self.date = date
        self.text = text
        self.creator = post_creator
        self.post_tags.extend(post_tags)


class Creator(Base):
    __tablename__ = 'creator'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    url = Column(String, unique=True)
    name = Column(String)

    def __init__(self, url, name):
        self.url = url
        self.name = name


class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    url = Column(String, unique=True)
    name = Column(String)

    def __init__(self, url, name):
        self.url = url
        self.name = name
