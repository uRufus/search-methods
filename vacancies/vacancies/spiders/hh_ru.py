from pprint import pprint

import scrapy

from vacancies.items import VacanciesItem


def parse_salary(salary):
    min_s, max_s, curr = None, None, None
    try:
        curr = salary.pop()
    except:
        salary = ''
    if 'По договорённости' in salary:
        pass
    elif not salary:
        pass
    elif 'до' in salary[0]:
        max_s = int(salary[1].replace(u'\u202f', u''))
    elif 'от' in salary[0]:
        min_s = int(salary[1].replace(u'\u202f', u''))
    elif '–' in salary[0]:
        salary = salary[0].split('–')
        min_s = int(salary[0].replace(' ', '').replace(u'\u202f', u''))
        max_s = int(salary[1].replace(' ', '').replace(u'\u202f', u''))
    return min_s, max_s, curr


class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?text=Python+developer']

    def parse(self, response):
        items = response.xpath("//div[@class='vacancy-serp-item-body__main-info']")
        next_page = response.xpath("//div[@class='pager']/a[@class='bloko-button']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for item in items:
            title = item.xpath(".//a[@class='serp-item__title']/text()").get()
            try:
                salary = item.xpath(".//span[@class='bloko-header-section-3']/text()").getall()
            except:
                salary = ''
            link = item.xpath(".//a[@class='serp-item__title']/@href").get()
            min_s, max_s, curr = parse_salary(salary)

            yield VacanciesItem(
                title=title,
                link=link,
                min_s=min_s,
                max_s=max_s,
                curr=curr,
            )
