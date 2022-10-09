from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from mvideo.spiders.test_mvideo import TestMvideoSpider


if '__name__' == '__main__':
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(TestMvideoSpider)
    reactor.run()


