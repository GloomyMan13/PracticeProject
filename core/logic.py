import os
import os.path as path
import requests
from requests.structures import CaseInsensitiveDict
from datetime import timedelta, date
import pandas as pd
from core.login import headers
from log_code.logs import exception

#  Lists with params. Needed in Getters.__setparam and in gui
RIGHT_SORT_LIST = ['subject', 'brand', 'name', 'size', 'barcode', 'articles']
ORDER_LIST = ['asc', 'desc']

#  Dict with key: url. Need for Getters.key
KEYS = {
        'orders': 'https://suppliers-api.wildberries.ru/api/v2/orders?',
        'costs': "https://suppliers-api.wildberries.ru/public/api/v1/info?",
        'stocks': "https://suppliers-api.wildberries.ru/api/v2/stocks?"
    }


class Getters:
    """
    Creates full request string for function and make request

    Attributes:
        key: str
             Key from KEYS to take url-link for request
        param_dict: dict
                    parameters of get request,
        head: CaseInsensitiveDict
              headers of get requests from login.py

    Methods:
        __init__(self): Initialize attributes
        __setparam: Takes key and needed params to create parameters
                    string for GET request
        __integer: Check by type(str(digits)) and create part of param string
        __string: Check by type(str) and create part of param string
        __date: Check by type(date) and reformat
                date into right format (RFC3339)
        __checker: Check needed of "&" sign between params
        response: Unit url, parameters, headers and return
                  result of request.get in JSON
    """

    # Keys with same parameters. Need for __setparam
    SAME_KEYS_LIST = ['gender', 'colors', 'countries', 'collections',
                      'seasons', 'contents', 'consists', 'options',
                      'si']

    @exception
    def __init__(self, key, param_dict, head=headers):
        """
        Initialize attributes

        Attributes:
            key: str
                 Key from KEYS to take url-link for request
            param_dict: dict
                        parameters of get request,
            head: CaseInsensitiveDict
                  headers of get requests from login.py
        """

        try:
            key = key.lower()
            self.link = KEYS[key]
        except KeyError:
            raise KeyError("Wrong keyword")
        except AttributeError:
            raise AttributeError('Key must be a string')

        if not isinstance(param_dict, dict):
            raise AttributeError('param_dict must be a dict')
        self.params = self.__setparam(key, param_dict)

        if isinstance(headers, requests.structures.CaseInsensitiveDict):
            self.headers = head
        else:
            raise ValueError('Headers must be a dict')

    @staticmethod
    @exception
    def __setparam(key, param_dict):
        """
        Takes key and needed params to create parameters
        string for GET request

        :return result: parameters string for GET request
        :rtype: str
        """

        result = ''
        if key == 'orders':
            STATUSES_LIST = [0, 1, 2, 3, 5, 6, 7]
            try:
                date_start = param_dict['date_start']
            except KeyError:
                date_start = (date.today() - timedelta(days=1))
            if isinstance(date_start, date):
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
                raise ValueError(f'Sort must be one of {RIGHT_SORT_LIST},'
                                 f'not {sort}')
            try:
                order = param_dict['order']
            except KeyError:
                order = None
            if order in ORDER_LIST:
                result += '&' + Getters.__string(order, 'order')
            elif order is not None and order not in ORDER_LIST:
                raise ValueError(f'Order must be one of {ORDER_LIST},'
                                 f'not {order}')
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
        return result

    @staticmethod
    @exception
    def __integer(param, param_name):
        """
        Check param by type and create part of param string

        :param param: parameter
        :type param: str(digits)
        :param param_name: name of parameter
        :type param_name: str
        """

        try:
            param = int(param)
        except ValueError:
            raise ValueError(f'{param_name} must be an int')
        result = f'{param_name}={param}'
        return result

    @staticmethod
    @exception
    def __string(param, param_name):
        """
        Check param by type(str) and create part of param string

        :param param: parameter
        :type param: str
        :param param_name: name of parameter
        :type param_name: str
        """

        if isinstance(param, str):
            result = f'{param_name}={param}'
        else:
            raise ValueError(f'{param_name} must be a string')
        return result

    @staticmethod
    @exception
    def __date(param, param_name):
        """
        Check by type(date) and reformat date into right format (RFC3339)

        :param param: Year, month and day
        :type param: date or None
        :param param_name: date_start or date_end
        :type param_name: str
        """

        if not isinstance(param, (date, type(None))):
            raise ValueError('date_end must be datetime.date or None obj')
        date_format = '%Y-%m-%dT'
        date_string = param.strftime(date_format)
        result = ''.join(f'{param_name}={date_string}' +
                         '00%3A00%3A00.000%2B10%3A00')
        return result

    @staticmethod
    def __checker(string):
        """
        Check needed of "&" sign between params

        :param string: parameter string
        :type string: str
        """
        if string != 0:
            string += '&'
        return string

    def response(self):
        """
        Unit url, parameters, headers and return
                  result of request.get in JSON

        :return: requests.get().json()
        :rtype: json
        """
        response = requests.get(self.link + self.params,
                                headers=self.headers)
        return response.json()


class Converter:
    """
    Class for convert json into xlsx

    Attributes:
        path: str
              path with filename
        key: str
             Function name
        json: jSON
              JSON array with results of Get request
    Methods:
        __init__: Initialize attributes
        __error_check: Check errors in JSON array,
                       takes needed fields from JSON
        convert: Creates dataset from JSON,
                 saves it to *.xlsx file by taken path
    """
    @exception
    def __init__(self, my_path, key, json):
        """
        Initialize attributes

        :param my_path: path with filename
        :type my_path: str
        :param key: Function name
        :type key: str
        :param json: JSON string with results of Get request
        :type json: JSON
        """
        self.path = path.normpath(my_path)

        if key in KEYS.keys():
            self.key = key
        else:
            raise AttributeError('Wrong command key')

        self.json = Converter.__error_check(json)

    @staticmethod
    @exception
    def __error_check(json):
        """
        Check errors in JSON array, takes needed fields from JSON

        :param json: JSON array with results of Get request
        :type json: JSON
        :return: Reformatted JSON array
        :rtype: JSON
        """
        json_keys = list(json.keys())
        if 'error' in json_keys:
            if json['error']:  # json['error'] have 2 args: True or False
                raise AttributeError(json['errorText'])
            elif json['data'] is None or json['data'] == []:
                raise ValueError('Data is none')
        else:
            json = json[json_keys[0]]
        return json

    def convert(self):
        """
        Creates dataset from JSON, saves it to *.xlsx file by taken path

        :return: 'Done'
        :rtype: str
        """
        dataset = pd.json_normalize(self.json)
        my_path = path.split(self.path)[0]
        if path.exists(my_path):
            dataset.to_excel(self.path)
        else:
            os.makedirs(my_path)
            dataset.to_excel(self.path)
        return 'Done'
