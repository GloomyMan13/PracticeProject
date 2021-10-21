import datetime
import json
from unittest import TestCase
from core.logic import Getters, Converter


class TestGetters(TestCase):
    def test_init(self):
        self.assertRaises(
                AttributeError, Getters, 1, {}
        )
        self.assertRaises(
            KeyError, Getters, '1', {}
        )

    def test_setparam(self):
        orders_dicts = [{'date_start': 5}, {'date_end': 13}, {'status': 'a'}]
        stocks_dicts = [{'sort': 'aaaa'}, {'order': 'aaaaaa'}]
        for diction in orders_dicts:
            self.assertRaises(
                ValueError, Getters, 'orders', diction
            )
        for diction in stocks_dicts:
            self.assertRaises(
                ValueError, Getters, 'stocks', diction
            )
        self.assertRaises(ValueError,
                          Getters, 'costs', {'quantity': 8})

    def test_integer(self):
        param = Getters('orders', {})
        self.assertRaises(
            ValueError,
            param._Getters__integer, 'aa', 'param'
        )
        self.assertEqual(
            'param=10',
            param._Getters__integer('10', 'param')
        )

    def test_string(self):
        param = Getters('orders', {})
        self.assertRaises(
            ValueError,
            param._Getters__string, 10, 'param'
        )
        self.assertEqual(
            'param=right',
            param._Getters__string('right', 'param')
        )

    def test_date(self):
        param = Getters('stocks', {})
        self.assertRaises(
            ValueError,
            param._Getters__date, '10-10-2021', 'date'
        )
        self.assertEqual(
            'date=2021-10-21T00%3A00%3A00.000%2B10%3A00',
            param._Getters__date(datetime.date.today(), 'date')
        )

    def test_checker(self):
        param = Getters('stocks', {})
        self.assertEqual('string&',
                         param._Getters__checker('string'))


class TestConverter(TestCase):
    def setUp(self):
        self.error_json1 = {'data': ['Some data'],
                            'error': True,
                            'errorText': 'Error'}
        self.error_json2 = {'data': [],
                            'error': False}
        self.error_json1 = json.dumps(self.error_json1)
        self.error_json1 = json.loads(self.error_json1)
        self.error_json2 = json.dumps(self.error_json2)
        self.error_json2 = json.loads(self.error_json2)

    def test_init(self):
        self.assertRaises(
            AttributeError,
            Converter, './', 10, self.error_json1
        )

    def test_error_check(self):

        self.assertRaises(
            AttributeError,
            Converter, './', 'orders', self.error_json1)
        self.assertRaises(
            ValueError,
            Converter, './', 'orders', self.error_json2
        )

    def tearDown(self):
        del(self.error_json2, self.error_json1)