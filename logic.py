import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime, timedelta
from login import headers
import tablib

KEYS = {
        'orders': 'https://suppliers-api.wildberries.ru/api/v2/orders?',
        'warehouses': "https://suppliers-api.wildberries.ru/api/v2/warehouses?",
        'costs': "https://suppliers-api.wildberries.ru/public/api/v1/info?",
        'stocks': "https://suppliers-api.wildberries.ru/api/v2/stocks?",
        'config': 'https://suppliers-api.wildberries.ru/api/v1/config/get/object/translated?',
        'search by pattern': "https://suppliers-api.wildberries.ru/api/v1/config/get/object/list?",
        'colors': 'https://suppliers-api.wildberries.ru/api/v1/directory/colors?',
        'gender': 'https://suppliers-api.wildberries.ru/api/v1/directory/kinds?',
        'countries': 'https://suppliers-api.wildberries.ru/api/v1/directory/countries?',
        'collections': 'https://suppliers-api.wildberries.ru/api/v1/directory/collections?',
        'seasons': 'https://suppliers-api.wildberries.ru/api/v1/directory/seasons?',
        'contents': 'https://suppliers-api.wildberries.ru/api/v1/directory/contents?',
        'consists': 'https://suppliers-api.wildberries.ru/api/v1/directory/consists?',
        'tnved': 'https://suppliers-api.wildberries.ru/api/v1/directory/tnved?',
        'options': 'https://suppliers-api.wildberries.ru/api/v1/directory/options?',
        'brands': 'https://suppliers-api.wildberries.ru/api/v1/directory/brands?',
        'si': 'https://suppliers-api.wildberries.ru/api/v1/directory/si?',
        'list': 'https://suppliers-api.wildberries.ru/api/v1/directory/get/list',
        'ext': 'https://suppliers-api.wildberries.ru/api/v1/directory/ext'
    }


class Getters:
    """
    Include objects with request.get

    :method __setparam: Chose function for generating parameter string, base on key arg
    :method __stocks: Generates parameter string for get.stocks
    :method __orders: Generates parameter string for get.orders
    :method __cost: Generates parameter string for get.costs
    :method response: Unit url, parameters, headers and return result of request.get in JSON
    """
    def __init__(self, key, head=headers, **kwargs):
        """
        :param key: Link for request, str
        :param head: headers of get requests, CaseInsensitiveDict
        :param params: parameters of get request, str
        """

        try:
            key = key.lower()
            self.link = KEYS[key]
        except KeyError:
            print("Wrong keyword")
        except AttributeError:
            print('Key must be a string')

        if isinstance(headers, requests.structures.CaseInsensitiveDict):
            self.headers = head
        else:
            raise ValueError('Headers must be a dict')
        self.params = self.__setparam(key, **kwargs)

    @staticmethod
    def __setparam(key, name=None, pattern=None, parent=None, subject=None, lang='ru', top=10, obj_id=None,
                   date_start=(datetime.today() - timedelta(days=1)), date_end=None, status=None, take=10, skip=0,
                   order_id=None, search=None, sort=None, order=None, quantity=1):
        """
        Takes key and needed params to create parameters string for GET request
        """
        result = ''
        if key == 'orders':
            STATUSES_LIST = [0, 1, 2, 3, 5, 6, 7]
            if isinstance(date_start, datetime):
                result = Getters.__date(date_start, 'date_start')
            else:
                raise ValueError('Date start must be a datetime object')
            if date_end is not None:
                result += '&' + Getters.__date(date_end, 'date_end')
            if status in STATUSES_LIST:
                result += '&' + status
            elif status is not None and status not in STATUSES_LIST:
                raise ValueError(f"Status must be one of {STATUSES_LIST}")
            result += '&' + Getters.__integer(take, 'take')
            result += '&' + Getters.__integer(skip, 'skip')
            if order_id is not None:
                result += '&' + Getters.__integer(order_id, 'id')
        elif key == 'stocks':
            RIGHT_SORT_LIST = ['subject', 'brand', 'name', 'size',
                               'barcode', 'articles']
            ORDER_LIST = ['asc', 'desc']
            if search is not None:
                result = Getters.__string(search, 'search')
            result += '&' + Getters.__integer(take, 'take')
            result += '&' + Getters.__integer(skip, 'skip')
            if sort in RIGHT_SORT_LIST:
                result += '&' + Getters.__string(sort, 'sort')
            elif sort is not None and sort not in RIGHT_SORT_LIST:
                raise ValueError(f'Sort must be one of {RIGHT_SORT_LIST}')
            if order in ORDER_LIST:
                result += '&' + Getters.__string(order, 'order')
            elif order is not None and order not in ORDER_LIST:
                raise ValueError(f'Order must be one of {ORDER_LIST}')
        elif key == 'costs':
            QUANTITY_LIST = [1, 2, 0]
            if quantity not in QUANTITY_LIST:
                raise ValueError('Quantity must be 1, 2 or 0')
            else:
                result.join(f'quantity={quantity}')
        elif key == 'config':
            return Getters.__string(name, 'name')
        elif key == 'search by pattern':
            if name is not None:
                result = Getters.__string(pattern, 'pattern')
            if parent is not None:
                result += Getters.__checker(result)
                result += Getters.__string(parent, 'parent')
            if lang == 'ru':
                result += "&" + Getters.__string(lang, 'lang')
            else:
                raise ValueError('Lang must be ru')
        elif key in Getters.SAME_KEYS_LIST:
            result = Getters.__integer(top, 'top')
            if pattern is not None:
                result += '&' + Getters.__string(pattern, 'pattern')
            if obj_id is not None:
                result += '&' + Getters.__integer(obj_id, 'id')
        elif key == 'list':
            return ''
        elif key == 'tnved':
            if obj_id is not None:
                result = Getters.__integer(obj_id, 'subjectID')
            if subject is not None:
                result += Getters.__checker(result)
                result += Getters.__string(subject, 'subject')
            if pattern is not None:
                result += Getters.__checker(result)
                result += Getters.__string(pattern, 'pattern')
        elif key == 'ext':
            result = Getters.__integer(top, 'top')
            if pattern is not None:
                result += '&' + Getters.__string(pattern, 'pattern')
            if obj_id is not None:
                result += '&' + Getters.__integer(obj_id, 'id')
            if pattern is not None:
                result += '&' + Getters.__string(pattern, 'option')
        return result

    @staticmethod
    def __integer(param, param_name):
        """
        Check by type and create part of param string
        """
        if isinstance(param, int):
            result = f'{param_name}={param}'
        else:
            raise ValueError(f'{param_name} must be an int')
        return result

    @staticmethod
    def __string(param, param_name):
        """
        Check by type and create part of param string
        """
        if isinstance(param, str):
            result = f'{param_name}={param}'
        else:
            raise ValueError(f'{param_name} must be a string')
        return result

    @staticmethod
    def __date(param, param_name):
        """
        Reformat datetime into right format (RFC3339)
        """
        date_format = '%Y-%m-%dT'
        date = param.strftime(date_format)
        result = ''.join(f'{param_name}={date}' +
                         '00%3A00%3A00.000%2B10%3A00')
        if not isinstance(param, (datetime, type(None))):
            raise ValueError('date_end must be datetime or None obj')
        return result

    @staticmethod
    def __checker(string):
        """
        Check needed of "&" sign between params
        """
        if string != 0:
            string += '&'
        return string

    def response(self):
        """
        Get responses from url with params

        :return: response in JSON format
        """
        response = requests.get(self.link + self.params,
                                headers=self.headers)
        return response.json()

    SAME_KEYS_LIST = ['gender', 'colors', 'countries', 'collections', 'seasons', 'contents',
                      'consists', 'options', 'si']


class Converter:
    def __init__(self, path, key, json):
        self.path = path
        self.key = key
        self.json = json

    def convert(self):
        dataset = tablib.Dataset()
        dataset.dict = self.json
        with open(self.path, 'wb') as file:
            file.write(dataset.xlsx)
        return 'Done'

