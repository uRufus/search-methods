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


def hh_search(text):
    # готовим данные для вызова сайта
    url = "https://hh.ru/search/vacancy"
    url_hh = "https://hh.ru/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    params = {
        'text': text,
        'from': 'suggest_post',
        'area': '1'
    }

    # Получаем в ответе html и преобразуем в beautiful soup
    response = requests.get(url=url, headers=headers, params=params)
    soup = bs(response.content, 'html.parser')

    # Собираем ссылки на страницы
    try:
        number_of_pages = soup.find("div", attrs={'class': ['pager']}).find_all('span')
    except:
        return []
    pages = []
    for p in number_of_pages:
        try:
            pages.append(int(p.text))
        except:
            pass

    pages.sort(reverse=True)

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
            max_s = salary[:-4].replace(' ', '')
            max_s = int(max_s.replace(' ', ''))
            curr = salary[-4:]
        elif 'от' in salary:
            salary = salary.replace('от', '')
            # min_s = int(salary[:-4].replace(' ', ''))
            min_s = salary[:-4].replace(' ', '')
            min_s = int(min_s.replace(' ', ''))
            curr = salary[-4:]
        elif '–' in salary:
            salary = salary.split('–')
            min_s = salary[0].replace(' ', '')
            min_s = int(min_s.replace(' ', ''))
            max_s = salary[1][:-4].replace(' ', '')
            max_s = int(max_s.replace(' ', ''))
            curr = salary[1][-4:]
        return min_s, max_s, curr


    # Считываем данные со страниц с результатами поиска
    for p in range(pages[0]):
        params['page'] = p
        params['hhtmFrom'] = 'vacancy_search_list'
        response = requests.get(url=url, headers=headers, params=params)
        soup = bs(response.content, 'html.parser')
        jobs = soup.find_all("div", attrs={'class': ['vacancy-serp-item-body__main-info']})
        for job in jobs:
            title = job.find('a', attrs={'class': ['serp-item__title']}).text # Вакансия
            try:
                salary = job.find('span', attrs={'class': ['bloko-header-section-3']}).text # ЗП
            except:
                salary = ''
            link = job.find('a', attrs={'class': ['serp-item__title']})['href'] # Ссылка
            min_s, max_s, curr = parse_salary(salary)
            vacancy = {
                'title': title,
                'min_salary': min_s,
                'max_salary': max_s,
                'currency': curr,
                'link': (url_hh + link),
                'site': url_hh
            }
            vacancies.append(vacancy)
    return vacancies

