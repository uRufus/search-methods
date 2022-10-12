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


class SuperjobRuSpider(scrapy.Spider):
    name = 'superjob_ru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://balashiha.superjob.ru/vacancy/search/?keywords=python%20developer']

    def parse(self, response):
        items = response.xpath("//div[@class='_2lp1U _2J-3z _3B5DQ']")
        next_page = response.xpath("//div[@class='pager']/a[@class='bloko-button']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for item in items:
            title = item.xpath(".//span[@class='_9fIP1 _249GZ _1jb_5 QLdOc']/text()").get()
            try:
                salary = item.xpath(".//span[@class='_2eYAG _1nqY_ _249GZ _1jb_5 _1dIgi']/text()").getall()
            except:
                salary = ''
            link = item.xpath(".//span[@class='_9fIP1 _249GZ _1jb_5 QLdOc']/a/@href").get()
            pprint(salary)
            min_s, max_s, curr = parse_salary(salary)

            yield VacanciesItem(
                title=title,
                link=link,
                min_s=min_s,
                max_s=max_s,
                curr=curr,
            )
