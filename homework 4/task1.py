'''
Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, которая будет добавлять только новые вакансии/продукты в вашу базу.

* Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты).

* Любая аналитика. Например matching ваканский с разных площадок
'''
from pprint import pprint
from pymongo import MongoClient
from hh import hh_search
from superjob import superjob_search


def get_vacancies(text):
    """функция для сбора вакансий с HH и superjob"""
    hh_list = hh_search(text)
    superjob_list = superjob_search(text)
    hh_list.extend(superjob_list)
    return hh_list


# собираем список вакансий
vacancies = get_vacancies('python developer new')

# подключаемся к БД
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client.vacanciesdb

# проверяем есть ли вакансия в БД и если нет добавляем туда
for v in vacancies:
    if not db.vacancies.count_documents({'title': v['title'],
                                         'min_salary': v['min_salary'],
                                         'max_salary': v['max_salary'],
                                         'currency': v['currency'],
                                         'link': v['link'],
                                         'site': v['site']
                                         }, limit=1):
        db.vacancies.insert_one(v)

# Выводит список вакансий
number = db.vacancies.find()
pprint(len(list(number)))


def get_vacancy_based_on_price(price):
    """Выводит список вакансий, больше определенной суммы:"""
    for doc in db.vacancies.find({'$or': [{'min_salary': {'$gt': price}}, {'max_salary': {'$gt': price}}]}):
        pprint(doc)


get_vacancy_based_on_price(200000)
# db.vacancies.drop()
