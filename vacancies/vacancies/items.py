# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VacanciesItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    min_s = scrapy.Field()
    max_s = scrapy.Field()
    curr = scrapy.Field()
    _id = scrapy.Field()
