"""
2. Работа будет состоять с недокументированным API. Нужно ввести релевантный запрос на сайте https://www.delivery-club.ru/search
(а) из предложенных точек с помощью API найти долю (в %) с бесплатной и платной доставкой. Для каждой категории рассчитать среднюю минимальную стоимость заказа.
(б) для каждой из категорий из пункта (а) рассчитать долю (в %) магазинов и ресторанов
"""

import requests

response = requests.get("https://api.delivery-club.ru/api1.2/vendors/search?latitude=55.700182&longitude=37.580158&query=%D0%BF%D0%B8%D1%86%D1%86%D0%B0&cacheBreaker=1663793177")

response = response.json()

# (а) из предложенных точек с помощью API найти долю (в %) с бесплатной и платной доставкой.
delivery = [0, 0]
for repo in response["vendors"]:
    if repo["delivery"]["price"]["value"] > 0:
        delivery[1] += 1
    else:
        delivery[0] += 1

print(f"Заведений с бесплатной доставкой {delivery[1]}.\n"
      f"Заведений с платной доставкой {delivery[0]}.\n"
      f"Всего заведений {delivery[0] + delivery[1]}.\n"
      f"Доля с бесплатной доставкой {delivery[1] / (delivery[0] + delivery[1]):.2f}.\n"
      f"Доля с платной доставкой {delivery[0] / (delivery[0] + delivery[1]):.2f}")

# Для каждой категории рассчитать среднюю минимальную стоимость заказа.
min_price = {}
for repo in response["vendors"]:
    if repo["categoryId"] in min_price:
        min_price[repo["categoryId"]].append(repo["delivery"]["minOrderPrice"]["value"])
    else:
        min_price[repo["categoryId"]] = [repo["delivery"]["minOrderPrice"]["value"]]

for category, price in min_price.items():
    print(f"Для категории {category} средняя минимальная стоимость заказа равна {sum(price)/len(price):.2f}.")

# (б) для каждой из категорий из пункта (а) рассчитать долю (в %) магазинов и ресторанов
shops = [0, 0]
for category, price in min_price.items():
    if category > 1:
        shops[1] += len(price)
    else:
        shops[0] += len(price)

print(f"Всего заведений {shops[0] + shops[1]}.\n"
      f"Доля магазинов {shops[0] / (shops[0] + shops[1]):.2f}")
