import os
import os.path as path
import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime, timedelta
import pandas as pd
from login import headers


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
        'list': 'https://suppliers-api.wildberries.ru/api/v1/directory/get/list'
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
    def __init__(self, key, param_dict, head=headers):
        """
        :param key: Link for request, str
        :param head: headers of get requests, CaseInsensitiveDict
        :param param_dict: parameters of get request, dict
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
        if not isinstance(param_dict, dict):
            raise AttributeError('param_dict must be a dict')
        self.params = self.__setparam(key, param_dict)

    @staticmethod
    def __setparam(key, param_dict):
        """name=None, pattern=None, parent=None, subject=None, lang='ru', top=1000, obj_id=None,
                   date_start=(datetime.today() - timedelta(days=1)), date_end=None, status=None, take=1000, skip=0,
                   order_id=None, search=None, sort=None, order=None, quantity=1):"""
        """
        Takes key and needed params to create parameters string for GET request
        """
        result = ''
        if key == 'orders':
            STATUSES_LIST = [0, 1, 2, 3, 5, 6, 7]
            try:
                date_start = param_dict['date_start']
            except KeyError:
                date_start = (datetime.today() - timedelta(days=1))
            if isinstance(date_start, datetime):
                result = Getters.__date(date_start, 'date_start')
            else:
                raise ValueError('Date start must be a datetime object')
            try:
                date_end = param_dict['date_end']
            except KeyError:
                date_end = None
            if date_end is not None:
                result += '&' + Getters.__date(date_end, 'date_end')
            try:
                status = param_dict['status']
            except KeyError:
                status = None
            if status in STATUSES_LIST:
                result += '&' + status
            elif status is not None and status not in STATUSES_LIST:
                raise ValueError(f"Status must be one of {STATUSES_LIST}")
            try:
                take = param_dict['take']
            except KeyError:
                take = 1000
            try:
                skip = param_dict['skip']
            except KeyError:
                skip = 0
            result += '&' + Getters.__integer(take, 'take')
            result += '&' + Getters.__integer(skip, 'skip')
            try:
                order_id = param_dict['order_id']
            except KeyError:
                order_id = None
            if order_id is not None:
                result += '&' + Getters.__integer(order_id, 'id')
        elif key == 'stocks':
            RIGHT_SORT_LIST = ['subject', 'brand', 'name', 'size',
                               'barcode', 'articles']
            ORDER_LIST = ['asc', 'desc']
            try:
                search = param_dict['search']
            except KeyError:
                search = None
            if search is not None:
                result = Getters.__string(search, 'search')
            try:
                take = param_dict['take']
            except KeyError:
                take = 1000
            try:
                skip = param_dict['skip']
            except KeyError:
                skip = 0
            result += '&' + Getters.__integer(take, 'take')
            result += '&' + Getters.__integer(skip, 'skip')
            try:
                sort = param_dict['sort']
            except KeyError:
                sort = None
            if sort in RIGHT_SORT_LIST:
                result += '&' + Getters.__string(sort, 'sort')
            elif sort is not None and sort not in RIGHT_SORT_LIST:
                raise ValueError(f'Sort must be one of {RIGHT_SORT_LIST}')
            try:
                order = param_dict['order']
            except KeyError:
                order = None
            if order in ORDER_LIST:
                result += '&' + Getters.__string(order, 'order')
            elif order is not None and order not in ORDER_LIST:
                raise ValueError(f'Order must be one of {ORDER_LIST}')
        elif key == 'costs':
            QUANTITY_LIST = [1, 2, 0]
            try:
                quantity = param_dict['quantity']
            except KeyError:
                quantity = 1
            if quantity not in QUANTITY_LIST:
                raise ValueError('Quantity must be 1, 2 or 0')
            else:
                result.join(f'quantity={quantity}')
        elif key == 'config':
            try:
                name = param_dict['name']
            except KeyError:
                raise ValueError("Name can't be None, operation meaningless")
            return Getters.__string(name, 'name')
        elif key == 'search by pattern':
            try:
                pattern = param_dict['pattern']
            except KeyError:
                pattern = None
            if pattern is not None:
                result = Getters.__string(pattern, 'pattern')
            try:
                parent = param_dict['parent']
            except KeyError:
                parent = None
            if parent is not None:
                result += Getters.__checker(result)
                result += Getters.__string(parent, 'parent')
            try:
                lang = param_dict['lang']
            except KeyError:
                lang = 'ru'
            if lang == 'ru':
                result += "&" + Getters.__string(lang, 'lang')
            else:
                raise ValueError('Lang must be ru')
        elif key in Getters.SAME_KEYS_LIST:
            try:
                top = param_dict['top']
            except KeyError:
                top = 1000
            result = Getters.__integer(top, 'top')
            try:
                pattern = param_dict['pattern']
            except KeyError:
                pattern = None
            if pattern is not None:
                result += '&' + Getters.__string(pattern, 'pattern')
            try:
                obj_id = param_dict['obj_id']
            except KeyError:
                obj_id = None
            if obj_id is not None:
                result += '&' + Getters.__integer(obj_id, 'id')
        elif key == 'list':
            return ''
        elif key == 'tnved':
            try:
                subj_id = param_dict['subjectID']
            except KeyError:
                subj_id = None
            if subj_id is not None:
                result = Getters.__integer(subj_id, 'subjectID')
            try:
                subject = param_dict['subject']
            except KeyError:
                subject = None
            if subject is not None:
                result += Getters.__checker(result)
                result += Getters.__string(subject, 'subject')
            try:
                pattern = param_dict['pattern']
            except KeyError:
                pattern = None
            if pattern is not None:
                result += Getters.__checker(result)
                result += Getters.__string(pattern, 'pattern')
        return result

    @staticmethod
    def __integer(param, param_name):
        """
        Check by type and create part of param string
        """
        try:
            param = int(param)
        except ValueError:
            raise ValueError(f'{param_name} must be an int')
        result = f'{param_name}={param}'
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
    """
    Converts
    """
    def __init__(self, my_path, key, json):
        self.path = path.normpath(my_path)
        if key in KEYS.keys():
            self.key = key
        else:
            raise AttributeError('Wrong command key')
        self.json = Converter.__keygen(self.key, json)

    @staticmethod
    def __keygen(key, json):
        json_keys = list(json.keys())
        if 'error' in json_keys:
            if json['error']:
                raise AttributeError(json['errorText'])
            elif json['data'] is None or json['data'] == []:
                raise ValueError('Data is none')
        else:
            EXCEPTION_LIST = ['config', 'search by pattern', 'colors', 'gender', 'countries', 'collections', 'seasons',
                              'contents', 'consists', 'tnved', 'options', 'brands', 'si', 'list']
            if key in EXCEPTION_LIST:
                json = json['data']
            else:
                json = json[json_keys[0]]
        return json

    def convert(self):
        dataset = pd.json_normalize(self.json)
        my_path = path.split(self.path)[0]
        if path.exists(my_path):
            dataset.to_excel(self.path)
        else:
            os.makedirs(my_path)
            dataset.to_excel(self.path)
        return 'Done'
