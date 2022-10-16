import scrapy

from leroy_merlin.items import LeroyMerlinItem
from scrapy.loader import ItemLoader


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/emali/']

    def parse(self, response):
        item_links = response.xpath("//a[@class='bex6mjh_plp b1f5t594_plp iypgduq_plp nf842wf_plp']/@href]").getall()
        for link in item_links:
            yield response.follow(link, callback=self.parse_goods)

        next_page = response.xpath("//div[@class='s1nb31eh_plp']/a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_goods(self, response):
        loader = ItemLoader(item=LeroyMerlinItem(), response=response)
        loader.add_xpath('title', ".//span[@class='t12nw7s2_pdp']/text()")
        loader.value('link', response.url)
        loader.add_xpath('price', ".//span[@slot='price']/text()")
        loader.add_xpath('curr', ".//span[@slot='currency']/text()")
        loader.add_xpath('photos', ".//media-carousel[@slot='media-content']/picture/source/@srcset")
        loader.load_item()
