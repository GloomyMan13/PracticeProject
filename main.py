from API.logic import Getters, GetObjectInfo
from API.login import headers

orders = 'colors'
get_orders = GetObjectInfo(orders, headers, pattern='Красный')
print(get_orders.response())

