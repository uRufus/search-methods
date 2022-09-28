"""
Написать приложение или функцию, которые собирают основные новости с сайта на выбор lenta.ru, yandex-новости.
Для парсинга использовать XPath.
Структура данных в виде словаря должна содержать:
- *название источника;
- наименование новости;
- ссылку на новость;
- дата публикации.
"""
from pprint import pprint
from lxml import html
import requests

# Сделал на примере игрового сайта
url = "https://stopgame.ru/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

response = requests.get(url=url, headers=headers)

dom = html.fromstring(response.text)

top_news = dom.xpath("//a[@class='_card_79oog_3 _card--big_79oog_1']")
latest_news = dom.xpath("//a[@class='_news-widget__item_1dwcg_268']")
main_news = dom.xpath("//ul[@class='_main-grid_1dwcg_1']/li")
news_list = []

for news in main_news:
    if news.xpath(".//article/section/section[@class='_card__content_1akif_357']/a/text()") != []:
        name = news.xpath(".//article/section/section[@class='_card__content_1akif_357']/a/text()")[0]
        link = news.xpath(".//article/a[@class='_card__image_1akif_1']/@href")
        if len(link) > 0:
            link = (url[:-1] + link[0])
        publish_date = news.xpath(".//article/section/section[@class='_card__info_1akif_1']/section[@class='_card__date_1akif_1']/text()")[0][1:]
    elif news.xpath(".//a/section[@class='_card__bottom_79oog_1']/div/span/text()") != []:
        name = news.xpath(".//a/section[@class='_card__bottom_79oog_1']/div/span/text()")[0]
        link = news.xpath(".//@href")
        if len(link) > 0:
            link = (url[:-1] + link[0])
        publish_date = None
    else:
        continue

    news_dict = {
        'source': 'StopGame.ru',
        'name': name,
        'link': link,
        'publish_date': publish_date
    }

    news_list.append(news_dict)

for news in top_news:
    name = news.xpath(".//span/text()")
    link = news.xpath("./@href")
    publish_date = None
    news_dict = {
        'source': 'StopGame.ru',
        'name': name[1],
        'link': (url[:-1] + link[0]),
        'publish_date': publish_date
    }

    news_list.append(news_dict)

for news in latest_news:
    name = news.xpath(".//span/text()")[4]
    link = news.xpath("./@href")
    publish_date = news.xpath(".//span/text()")[0]
    news_dict = {
        'source': 'StopGame.ru',
        'name': name[1:],
        'link': (url[:-1] + link[0]),
        'publish_date': publish_date[1:]
    }

    news_list.append(news_dict)

pprint(news_list)
