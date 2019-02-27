# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GbblogparseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BlogPost(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    post_img = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
    text = scrapy.Field()
    post_creator = scrapy.Field()
    tags = scrapy.Field()
    image_path = scrapy.Field()


class PostCreator(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()


class Tag(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
