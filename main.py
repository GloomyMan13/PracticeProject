from logic import Getters, Converter
from login import headers
gender = 'orders'
url = "https://suppliers-api.wildberries.ru/card/list"
get_orders = Getters(gender, headers)
#new_file = open("NewXLS.xlsx", 'w')
print(get_orders.response())
new_file = Converter(path="NewXLS.xlsx", key=None, json=get_orders.response()['orders'])
new_file.convert()
