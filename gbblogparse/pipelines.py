# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from db import database
from sqlalchemy.exc import IntegrityError
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class GbblogparsePipeline(object):

    def process_item(self, item, spider):
        session = database.get_session()
        creator = database.set_creator(session, **item['post_creator'])
        tags = database.set_tags(session, *item['tags'])
        item['post_creator'] = creator
        item['tags'] = tags

        blog_post = database.set_post(session, **item)

        try:
            session.commit()
        except IntegrityError:
            print(f"Dublicate {blog_post.title}")
        finally:
            session.close()
        return item


class BlogImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['post_img']:

            try:
                yield scrapy.Request(item['post_img'])
            except TypeError:
                return None

    def item_completed(self, results, item, info):
        if results and results[0][0]:
            image_path = results[0][1]['path']
            item['image_path'] = image_path
        else:
            item['image_path'] = None

        return item
