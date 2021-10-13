import _tkinter
import datetime
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkcalendar import Calendar
import errors
import logic
import login

params = {
        'orders': ['date_start', 'date_end', 'status', 'take', 'skip', 'order_id'],
        'warehouses': None,
        'costs': ['quantity'],
        'stocks': ['search', 'sort', 'order'],
        'config': ['name'],
        'search by pattern': ['name', 'parent', 'lang'],
        'tnved': ['obj_id', 'subject', 'pattern'],
        'list': [],
        'colors': ['top', 'pattern', 'id'],
        'gender': ['top', 'pattern', 'id'],
        'collections': ['top', 'pattern', 'id'],
        'seasons': ['top', 'pattern', 'id'],
        'contents': ['top', 'pattern', 'id'],
        'consists': ['top', 'pattern', 'id'],
        'options': ['top', 'pattern', 'id'],
        'brands': ['top', 'pattern', 'id'],
        'si': ['top', 'pattern', 'id']
    }

keys_list = list(params.keys())

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('JSON to EXCEL')
        self.geometry('600x100')
        self.text = tk.Text(self, height=10, width=50)
        self.new_file = None
        self.path_txt = tk.Label(self)
        self.path_txt.grid(column=4, row=1)

        label_text = tk.StringVar()
        label_text.set('Choose operation:')

        label = tk.Label(textvar=label_text, font=('Arial', 9))
        label.grid(column=0, row=1, padx=10)

        self.func_box = Combobox()
        self.func_box['values'] = keys_list
        self.func_box.current(0)
        self.func_box.grid(column=1, row=1, padx=10)

        file_button = tk.Button(self, text="Choose file", command=self.save_file)
        file_button.grid(column=3, row=1, padx=20)

        next_button = tk.Button(self, text='Next', command=self.start)
        next_button.grid(column=3, row=2)

        quit_button = tk.Button(self, text='Quit', command=self.exit)
        quit_button.grid(column=0, row=2)

    def save_file(self):
        self.new_file = filedialog.asksaveasfile(title="Save file",
                                                 defaultextension=".xlsx",
                                                 filetypes=(("Excel files", ".xlsx"),
                                                            ("all files", "*.*")))
        if self.new_file:
            string = str(self.new_file).replace("<_io.TextIOWrapper name='", '')
            del_index = string.index("' mode")
            string = string[0:del_index]
            self.path_txt.configure(text=string)
            self.new_file = string

    def start(self):
        if self.new_file is None:
            msgbox.showerror("ERROR", 'Filepath is not specified')
        elif self.func_box.get() == 'orders':
            wind = Orders(self.func_box.get(), self.new_file)
            wind.mainloop()

    def exit(self):
        if msgbox.askokcancel("Close app?", "Would you like to close an app?"):
            self.destroy()
        else:
            pass


class CalendarDialog(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")

        self.cal = Calendar(self, selectmode='day')
        self.cal.grid(column=1, row=0)

        self.result = None

        tk.Button(self, text="Check Date", command=self.check_date).grid(column=1, row=2)
        tk.Button(self, text='Ok and exit', command=self.ok_and_exit).grid(column=2, row=2)

        self.date = tk.Label(self, text="")
        self.date.grid(column=1, row=1)

    def check_date(self):
        self.date.config(text="Selected Date is: " + self.cal.get_date())

    def ok_and_exit(self):
        self.result = self.cal.selection_get()
        return self.result, self.destroy()


class Widgets(tk.Toplevel):
    def __init__(self, key, path):
        super().__init__()
        self.key = key
        self.path = path
        self.param_dict = {}

        self.goodbye_button = tk.Button(self, text='Cancel', command=self.cancel)
        self.goodbye_button.grid(column=0, row=4)

        self.start_button = tk.Button(self, text='Start', command=self.start_convert)
        self.start_button.grid(column=3, row=4)

        self.valid_num_command = self.register(self.only_num)

        row = 0
        column = 0
        for element in params[self.key]:
            el_key = element
            if isinstance(element, dict):
                el_key = list(element.keys())[0]
            labeltext = el_key.replace('_', ' ')
            labeltext[0].upper()
            new_label = tk.Label(self, text=labeltext)
            new_label.grid(column=column, row=row)
            row += 1
            if row > 3:
                row = 0
                column += 2

    def only_num(self, take):
        if take.isdigit():
            if int(take) >= 0:
                return True
            else:
                msgbox.showerror('Input error', 'Digit must be more or equal than 0')
                raise UserWarning('Try to input "-" digit')
        else:
            msgbox.showerror("Input Error", "Only digits here")
            raise UserWarning("Try to input char in field take or skip")

    def cancel(self):
        if msgbox.askokcancel('Close window?', 'Close window?'):
            self.destroy()
        else:
            pass

    def start_convert(self):
        msgbox.showerror("Start", f"Starting with params: \n {self.param_dict} \n Func must be reassigned!")
        raise PermissionError('Func must be reassigned')


class Orders(Widgets):
    def __init__(self, key, path):
        super().__init__(key, path)
        STATUSES_LIST = [0, 1, 2, 3, 5, 6, 7]

        calendar_start_butt = tk.Button(self, text='Choose date', command=lambda: self.get_date('date_start'))
        calendar_start_butt.grid(column=1, row=0)

        calendar_end_butt = tk.Button(self, text='Choose date', command=lambda: self.get_date('date_end'))
        calendar_end_butt.grid(column=1, row=1)

        self.status_box = Combobox(self)
        self.status_box['values'] = STATUSES_LIST
        self.status_box.grid(column=1, row=2)

        self.take_num = tk.Entry(self, validate='key', validatecommand=(self.valid_num_command, '%S'))
        self.take_num.grid(column=1, row=3)
        self.take_num.insert(0, 1000)

        self.skip_num = tk.Entry(self, validate='key', validatecommand=(self.valid_num_command, '%S'))
        self.skip_num.grid(column=3, row=0)
        self.skip_num.insert(0, 0)

        self.id_num = tk.Entry(self, validate='key', validatecommand=(self.valid_num_command, '%S'))
        self.id_num.grid(column=3, row=1)

    def get_date(self, key):
        cal = CalendarDialog()
        self.wait_window(cal)
        result = cal.result
        if key == 'date_start':
            if result > datetime.date.today():
                msgbox.showerror("Date error", "Start date must be today or earlier")
                raise errors.StartDateAttributeError(result)
        self.param_dict[key] = result

    def __param_checker(self):
        keys = list(self.param_dict.keys())
        if 'date_start' in keys and 'date_end' in keys:
            if self.param_dict['date_start'] > self.param_dict['date_end']:
                msgbox.showerror("Date Differ error", "Date start must be earlier, then date end")
                raise errors.DateDifferError()
        take_skip_differ = (int(self.param_dict['take']) - int(self.param_dict['skip']))
        if 1 > take_skip_differ or take_skip_differ > 1000:
            msgbox.showerror('Take And Skip differ error', 'Differ between take and skip must be between 1000 and 0')
            raise errors.TakeAndSkipDifferError(self.param_dict['take'], self.param_dict['skip'])
        return True

    def start_convert(self):
        try:
            self.param_dict['status'] = self.status_box.selection_get()
        except _tkinter.TclError:
            self.param_dict['status'] = None
        if self.take_num.get() != '':
            self.param_dict['take'] = self.take_num.get()
        if self.skip_num.get() != '':
            self.param_dict['skip'] = self.skip_num.get()
        if self.id_num.get() != '':
            self.param_dict['order_id'] = self.id_num.get()
        if Orders.__param_checker(self):
            msgbox.showinfo("Ok", f"Ok, {self.param_dict}, starting...")
            request = logic.Getters('orders', self.param_dict, login.headers)
            logic.Converter(self.path, 'orders', request.response()).convert()
            question = msgbox.askquestion("Another request?", "Want you create order request with another params?")
            if question == 'yes':
                pass
            else:
                self.destroy()



