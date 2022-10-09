import scrapy

from mvideo.items import MvideoItem


class TestMvideoSpider(scrapy.Spider):
    name = 'test_mvideo'
    allowed_domains = ['mvideo.ru']
    start_urls = ['https://mvideo.ru/promo/luchshie-predlojeniya?from=under_search']

    def parse(self, response):
        promo_categories = response.xpath("//div[@class='bp__menu-container']/a")
        for promo in promo_categories:
            link = promo.xpath(".//@href").get()
            yield response.follow(link, callback=self.parse_promo_items)

    def parse_promo_items(self, response):
        category = response.xpath("//h2[@class='fl-h2 u-inline']/text()").get()
        category = category.replace(' ', ' ')
        items = response.xpath("//div[@class='product-tiles-list-wrapper product-tiles-list_with-banner']/div[@class='fl-product-tile c-product-tile ']")
        next_page = response.xpath("//a[@class='c-pagination__next font-icon icon-up ']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_promo_items)

        for item in items:
            name = item.xpath(".//a[@class='fl-product-tile-title__link sel-product-tile-title']/text()").get()
            price = item.xpath(".//span[@class='fl-product-tile-price__current']/text()").get()
            name = name.replace(' ', ' ')
            price = price.replace('\t', '').replace(' ', ' ')
            yield MvideoItem(
                category=category,
                name=name,
                price=price
            )


