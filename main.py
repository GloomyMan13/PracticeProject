from logic import Getters, GetObjectInfo
from login import headers

gender = 'colors'

get_orders = GetObjectInfo(gender, headers)
print(get_orders.response())

