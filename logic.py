import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime, timedelta
from login import headers


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
            self.link = self.__KEYS[key]
        except KeyError:
            print("Wrong keyword")
        except AttributeError:
            print('Key must be a string')

        if isinstance(headers, requests.structures.CaseInsensitiveDict):
            self.headers = head
        else:
            raise ValueError('Headers must be a dict')
        self.params = self._setparam(key, **kwargs)

    @staticmethod
    def _setparam(key, **kwargs):
        if key == 'orders':
            return Getters.__orders(**kwargs)
        elif key == 'stocks':
            return Getters.__stocks(**kwargs)
        elif key == 'costs':
            return Getters.__cost(**kwargs)

    @staticmethod
    def __stocks(search=None, skip=0, take=10, sort=None, order=None):
        """
        Create parameters string for get_stocks

        :param search: None or str
               Word or word fragment to search
        :param skip: int
               How much strings to skip (pagination)
        :param take: int
               How much strings to take (pagination)
        :param sort: None or name of field to sort str(subject,
                     brand, name, size, barcode, articles)
               On which field sort
        :param order: None or str(asc) or str(desc)
               Order of sort: asc or desc
        :return: str
                parameters for get_stocks
        """
        param = '?'
        RIGHT_SORT_LIST = ['subject', 'brand', 'name', 'size',
                           'barcode', 'articles']
        ORDER_LIST = ['asc', 'desc']
        if isinstance(search, str):
            param += ''.join(f'search={search}&')
        elif not isinstance(search, (str, type(None))):
            raise ValueError("search must be a str")
        if not isinstance(skip, int):
            raise ValueError('skip must be an int')
        if not isinstance(take, int):
            raise ValueError('take must be an int')
        param += ''.join(f'skip={skip}&take={take}')
        if sort in RIGHT_SORT_LIST:
            param += ''.join(f'&sort={sort}')
        elif sort is not None and sort not in RIGHT_SORT_LIST:
            raise ValueError("sort must be subject, brand, name,"
                             "size, barcode or articles")
        if order in ORDER_LIST:
            param += ''.join(f'&order={order}')
        elif order is not None and order not in ORDER_LIST:
            raise ValueError("order must be asc or desc")
        return param

    @staticmethod
    def __orders(date_start=(datetime.today() - timedelta(days=1)), date_end=None, status=None, take=10, skip=0,
                 order_id=None):
        """
        Create parameter string for get_order

        :param date_start:  None or datetime obj
               Date of starting of search, if None - yesterday
        :param date_end: None or datetime obj
               Date of ending of search, if None - now
        :param status: None or int from 0 to 8 without 4
               If None - all
               0 = new order; 1 = accepted order; 2 = End of assembly task
               3 = Declined assembly task; 5 = On delivery; 6 = Client taken delivery;
               7 = Client refused to take delivery
        :param take: None or int
               If None = 10
               Num of taken orders (pagination)
        :param skip: int
               If None = 0
               Num of skipped orders (pagination)
        :param order_id: None or int
               Number of order
        :return: str
                 string of parameters
        """
        param = '?'
        STATUSES_LIST = [0, 1, 2, 3, 5, 6, 7]
        date_format = '%Y-%m-%dT'  # formatting time into RFC3339
        if not isinstance(date_start, datetime):
            raise ValueError("date_start must be datetime obj")
        date_start = date_start.strftime(date_format)
        param += ''.join(f'date_start={date_start}' +
                         '00%3A00%3A00.000%2B10%3A00')
        if isinstance(date_end, datetime):
            date_end = date_end.strftime(date_format)
            param += ''.join(f'&date_end={date_end}' +
                             '00%3A00%3A00.000%2B10%3A00')
        elif not isinstance(date_end, (datetime, type(None))):
            raise ValueError('date_end must be datetime obj')
        if status in STATUSES_LIST:
            param += ''.join(f'&status={status}')
        elif status is not None and status not in STATUSES_LIST:
            raise ValueError('status must be int in range from 0 to 7')
        if not isinstance(take, int):
            raise ValueError('take must be an int')
        if not isinstance(skip, int):
            raise ValueError('skip must be an int')
        param += ''.join(f'&skip={skip}&take={take}')
        if isinstance(order_id, int):
            param += ''.join(f'&id={order_id}')
        elif not isinstance(order_id, (int, type(None))):
            raise ValueError('order_id must be an int')
        return param

    @staticmethod
    def __cost(quantity=1):
        """
        Create parameters string to get_cost obj

        :param quantity:  0 - all, 1 - not null quantity, 2 - null quantity
        :return: parameter string
        """
        param = ''
        QUANTITY_LIST = [1, 2, 0]
        if quantity not in QUANTITY_LIST:
            raise ValueError('Quantity must be 1, 2 or 0')
        else:
            param.join(f'quantity={quantity}')
        return param

    def response(self):
        """
        Get responses from url with params

        :return: response in JSON format
        """
        response = requests.get(self.link + self.params,
                                headers=self.headers)
        return response.json()

    __KEYS = {
        'orders': 'https://suppliers-api.wildberries.ru/api/v2/orders',
        'warehouses': "https://suppliers-api.wildberries.ru/api/v2/warehouses",
        'costs': "https://suppliers-api.wildberries.ru/public/api/v1/info",
        'stocks': "https://suppliers-api.wildberries.ru/api/v2/stocks"
    }


class GetObjectInfo:
    def __init__(self, key, head=headers, **params):
        try:
            key = key.lower()
            self.link = self.__KEYS[key]
        except KeyError:
            print("Wrong keyword")
        except AttributeError:
            print('Key must be a string')
        if isinstance(headers, requests.structures.CaseInsensitiveDict):
            self.headers = head
        else:
            raise ValueError('Headers must be a dict')
        self.params = self.__setparam(key, **params)

    @staticmethod
    def __setparam(key, name1=None, name2=None, lang='ru', top=10, obj_id=None):
        result = ''
        if key == 'config':
            return GetObjectInfo.__string(name1, 'name')
        elif key == 'search by pattern':
            if name1 is not None:
                result = GetObjectInfo.__string(name1, 'pattern')
            if name2 is not None:
                result += GetObjectInfo.__checker(result)
                result += GetObjectInfo.__string(name2, 'parent')
            result += "&" + GetObjectInfo.__string(lang, 'lang')
            return result
        elif key in GetObjectInfo.SAME_KEYS_LIST:
            result = GetObjectInfo.__integer(top, 'top')
            if name1 is not None:
                result += '&' + GetObjectInfo.__string(name1, 'pattern')
            if obj_id is not None:
                result += '&' + GetObjectInfo.__integer(obj_id, 'id')
            return result
        elif key == 'list':
            return ''
        elif key == 'tnved':
            if obj_id is not None:
                result = GetObjectInfo.__integer(obj_id, 'subjectID')
            if name1 is not None:
                result += GetObjectInfo.__checker(result)
                result += GetObjectInfo.__string(name1, 'subject')
            if name2 is not None:
                result += GetObjectInfo.__checker(result)
                result += GetObjectInfo.__string(name2, 'pattern')
            return result
        elif key == 'ext':
            result = GetObjectInfo.__integer(top, 'top')
            if name1 is not None:
                result += '&' + GetObjectInfo.__string(name1, 'pattern')
            if obj_id is not None:
                result += '&' + GetObjectInfo.__integer(obj_id, 'id')
            if name2 is not None:
                result += '&' + GetObjectInfo.__string(name2, 'option')
            return result

    @staticmethod
    def __integer(param, param_name):
        if isinstance(param, int):
            result = f'{param_name}={param}'
        else:
            raise ValueError(f'{param_name} must be an int')
        return result

    @staticmethod
    def __string(param, param_name):
        if isinstance(param, str):
            result = f'{param_name}={param}'
        else:
            raise ValueError(f'{param_name} must be a string')
        return result

    @staticmethod
    def __checker(string):
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

    __KEYS = {
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
        'ext': 'https://suppliers-api.wildberries.ru/api/v1/directory/ext',
              }
