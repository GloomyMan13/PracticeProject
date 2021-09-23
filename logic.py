import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime, timedelta
from API.login import headers


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
        self.params = self._setparam(key, **params)

    @staticmethod
    def _setparam(key, **params):
        if key == 'config':
            return GetObjectInfo.__config(**params)
        elif key == 'search by pattern':
            return GetObjectInfo.__search_by_pattern(**params)
        elif key == 'colors':
            return GetObjectInfo.__colors(**params)
        elif key == 'gender':
            return GetObjectInfo.__gender(**params)

    @staticmethod
    def __config(name):
        if isinstance(name, str):
            return f'name={name}'
        else:
            raise ValueError('Name must be a string')

    @staticmethod
    def __search_by_pattern(name, parent, lang='ru'):
        if all(isinstance(x, str) for x in (name, parent, lang)):
            result = ''.join(f'pattern={name}&lang={lang}&parent={parent}')
            return result
        else:
            raise ValueError('All args must be a string')

    @staticmethod
    def __colors(top=100, pattern=None, obj_id=None):
        if isinstance(top, int):
            result = ''.join(f'top={top}')
        else:
            raise ValueError('tom must be an int')
        if isinstance(pattern, str):
            result += ''.join(f'&pattern={pattern}')
        elif not isinstance(pattern, (str, type(None))):
            raise ValueError('Pattern must be string or none')
        if isinstance(obj_id, int):
            result += ''.join(f'&{obj_id}')
        elif not isinstance(obj_id, (int, type(None))):
            raise ValueError('Id must be an int')
        return result

    def response(self):
        """
        Get responses from url with params

        :return: response in JSON format
        """
        response = requests.get(self.link + self.params,
                                headers=self.headers)
        return response.json()

    __KEYS = {
        'config': 'https://suppliers-api.wildberries.ru/api/v1/config/get/object/translated?',
        'search by pattern': "https://suppliers-api.wildberries.ru/api/v1/config/get/object/list?",
        'colors': 'https://suppliers-api.wildberries.ru/api/v1/directory/colors?',
        'gender': 'https://suppliers-api.wildberries.ru/api/v1/directory/kinds?'
              }
