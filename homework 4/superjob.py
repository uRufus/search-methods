"""
Собрать информацию о вакансиях на вводимую должность с сайтов hh.ru и/или Superjob и/или работа.ру.
Приложение должно анализировать несколько страниц сайта. Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (дополнительно: разносим в три поля: минимальная и
максимальная и валюта. цифры преобразуем к цифрам).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с всех сайтов. Общий результат можно вывести с
помощью dataFrame через pandas, сохранить в json, либо csv.
"""

from bs4 import BeautifulSoup as bs
import requests

def superjob_search(text):
    # готовим данные для вызова сайта
    url = "https://www.superjob.ru/vacancy/search/"
    url_superjob = "https://www.superjob.ru"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    params = {
        'keywords': text
    }

    # Получаем в ответе html и преобразуем в beautiful soup
    response = requests.get(url=url, headers=headers, params=params)
    soup = bs(response.content, 'html.parser')

    # Собираем ссылки на страницы
    number_of_pages = soup.select("a._1IHWd._6Nb0L._37aW8")
    pages = set([(url_superjob + p['href']) for p in number_of_pages])
    pages = [url] if pages == set() else pages

    # Создаем пустой список с вакансиями
    vacancies = []

    # Функция для парсинга зарплаты
    def parse_salary(salary):
        salary = salary.replace(u'\xa0', u' ')
        min_s, max_s, curr = None, None, None
        if 'По договорённости' in salary:
            pass
        elif 'до' in salary:
            salary = salary.replace('до', '')
            max_s = int(salary[:-4].replace(' ', ''))
            curr = salary[-4:]
        elif 'от' in salary:
            salary = salary.replace('от', '')
            min_s = int(salary[:-4].replace(' ', ''))
            curr = salary[-4:]
        elif '—' in salary:
            salary = salary.split('—')
            min_s = int(salary[0].replace(' ', ''))
            max_s = int(salary[1][:-4].replace(' ', ''))
            curr = salary[1][-4:]
        return min_s, max_s, curr


    # Считываем данные со страниц с результатами поиска
    for p in pages:
        response = requests.get(url=p, headers=headers)
        soup = bs(response.content, 'html.parser')
        jobs = soup.find_all("div", attrs={'class': ['_2lp1U _2J-3z _3B5DQ']})
        for job in jobs:
            title = job.find('span', attrs={'class': ['_9fIP1 _249GZ _1jb_5 QLdOc']}).find('a').text # Вакансия
            salary = job.find('span', attrs={'class': ['_2eYAG _1nqY_ _249GZ _1jb_5 _1dIgi']}).text # ЗП
            link = job.find('span', attrs={'class': ['_9fIP1 _249GZ _1jb_5 QLdOc']}).find('a')['href'] # Ссылка
            min_s, max_s, curr = parse_salary(salary)
            vacancy = {
                'title': title,
                'min_salary': min_s,
                'max_salary': max_s,
                'currency': curr,
                'link': (url_superjob + link),
                'site': url_superjob
            }
            vacancies.append(vacancy)
    return vacancies

