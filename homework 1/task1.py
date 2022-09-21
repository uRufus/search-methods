"""
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.
"""

import json
import requests


def json_file(file, repo):
    with open(file, 'w') as fp:
        json.dump(repo, fp)


user = "uRufus"

response = requests.get(f"https://api.github.com/users/{user}/repos")

response = response.json()

repositories = [{repo["name"]:repo["html_url"]} for repo in response]

# Создаем json файл со всеми данными по репозиториям
json_file("all_data.json", response)

# Создаем json файл со списком репозиториев
json_file("repos.json", repositories)
