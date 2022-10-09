# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MvideoItem(scrapy.Item):
    # # define the fields for your item here like:
    # # name = scrapy.Field()
    # pass
    category = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    _id = scrapy.Field()
