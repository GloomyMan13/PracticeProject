from unittest import TestCase
from datetime import datetime, timedelta
from log_code import errors
from core.gui import Window, Widgets


class TestWindow(TestCase):
    def test_start(self):
        window = Window()
        self.assertRaises(FileNotFoundError, window.start)
        window.new_file = 'D/docs/excel/xlsx'
        self.assertTrue(window.start)
        window.quit()


class TestWidgets(TestCase):
    def setUp(self):
        self.widget_date = Widgets('orders', 'some path')
        self.widget_date.param_dict = {'take': 1000, 'skip': 0,
                                       'date_start': datetime.now(),
                                       'date_end': (datetime.now() -
                                                    timedelta(days=3))}
        self.widget_take = Widgets('orders', 'some path')
        self.widget_take.param_dict = {'take': 10000, 'skip': 0}
        self.ok_widget = Widgets('orders', 'some path')
        self.ok_widget.param_dict = {'take': 1000, 'skip': 0,
                                     'date_start': datetime.now(),
                                     'date_end': (datetime.now() +
                                                  timedelta(days=3))}

    def test_init(self):
        try:
            widget = Widgets('wrong', 'some')
        except KeyError:
            pass

    def test_param_checker(self):
        self.assertRaises(errors.DateDifferError,
                          self.widget_date.param_checker)
        self.widget_date.quit()
        self.assertRaises(errors.TakeAndSkipDifferError,
                          self.widget_take.param_checker)
        self.assertTrue(self.ok_widget.param_checker)

    def test_only_num(self):
        self.assertTrue(self.ok_widget.only_num, '7')
        self.assertRaises(UserWarning, self.ok_widget.only_num, '-7')
        self.assertRaises(UserWarning, self.ok_widget.only_num, 'a')

    def test_start_convert(self):
        self.assertRaises(PermissionError, self.ok_widget.start_convert)
