from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from gbblogparse import settings
from gbblogparse.spiders.gbblog import GbblogSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(GbblogSpider)
    process.start()