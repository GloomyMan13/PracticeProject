from datetime import datetime
import logic
from logic import Getters, Converter
from login import headers
from gui import Window
import tkinter as tk


if __name__ == "__main__":
    window = Window()
    window.mainloop()


"""
gender = 'gender'
pattern = ''
get_orders = Getters(gender, headers, name='Шампуни', pattern=pattern, subject='Шампуни')
path = f'docs\docspath\{gender}.xlsx'
try:
    new_file = Converter(my_path=path, key=gender, json=get_orders.response())
    new_file.convert()
    print(f'{gender} done')
except AttributeError:
    raise AttributeError(f'{gender} error')
"""