# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LeroyMerlinItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    photos = scrapy.Field()
    curr = scrapy.Field()
    _id = scrapy.Field()
