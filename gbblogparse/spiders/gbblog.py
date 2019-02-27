# -*- coding: utf-8 -*-

import scrapy
from ..items import BlogPost, PostCreator, Tag


class GbblogSpider(scrapy.Spider):
    name = 'gbblog'
    allowed_domains = ['geekbrains.ru']
    start_urls = ['https://geekbrains.ru/posts']

    def parse_page(self, response):
        domain = 'https://geekbrains.ru'

        blogpost = BlogPost(
            url=response.url,
            title=response.css('h1.blogpost-title::text').get(),
            post_img=response.css('div.blogpost-content p img').xpath('@src').get(),
            description=response.css('div.blogpost-description span::text').get(),
            text=response.css('div.blogpost-content').get(),
            date=response.css('div.m-t-md').xpath('./span/@datecreated').get(),
            post_creator=PostCreator(
                name=response.css('div.padder-v').xpath('./@creator').get(),
                url=f"{domain}{response.css('div.padder-v a::attr(href)').get()}",
            ),
            tags=[Tag(name=itm.css('a::text').get(), url=f"{domain}{itm.css('a::attr(href)').get()}") for itm in
                  response.css("div.blogpost a.small")]
        )

        yield blogpost

    def get_paginator(self, response):
        max_pages = max([int(itm.split('=')[1]) for itm in response.css("a::attr(href)").extract()])
        pages = [f'/posts?page={itm}' for itm in range(2, max_pages + 1)]

        return pages

    def get_next_page(self, response):
        next_page = response.xpath('//a[@rel=$next]', next='next')

        return next_page[-1]

    def parse(self, response):
        paginator = response.css("ul.gb__pagination li")
        next_page = self.get_next_page(paginator)

        yield response.follow(next_page, callback=self.parse)

        for item in response.css("div.post-items-wrapper div.post-item"):
            link = item.css('a::attr(href)').extract_first()
            yield response.follow(link, callback=self.parse_page)
