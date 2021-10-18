import datetime
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as msgbox
from tkinter.ttk import Combobox
import requests
from tkcalendar import Calendar
from log_code import errors
from log_code.logs import exception
from core import logic

PARAMS = {
        'orders': ['date_start', 'date_end', 'status', 'take',
                   'skip', 'order_id'],
        'stocks': ['search', 'take', 'skip', 'sort', 'order'],
        'costs': ['quantity']
    }

keys_list = list(PARAMS.keys())


class Window(tk.Tk):
    """
    Main window class, inherit tkinter.Tk()

    Attributes:
        self.title: str
                    title of window
        self.geometry: str
                       window size
        text: tk.Text
              places path to window
        new_file: str
                  contains path
    Widgets:
        path_txt: tkinter.Label
                  Used for print chosen path
        op_label: tkinter.Label
                  Label before operation choose
        func_box: tkinter.ttk.Combobox
                  Used for choose function
        file_button: tkinter.Button
                     Used for path choose
        next_button: tkinter.Button
                     Used for opening sub-window with function params
        quit_button: tkinter.Button
                     Quit button
    Methods:
        __init__(self): Initialize attributes and widgets
        save_file(self): Starts filedialog, reformat received string into path
        start(self): Opens sub-window with function and
                     give func name with path
        exit(self): Overrides method tkinter.Tk.destroy()
                    Open sub-window with ask of exit.
                    If yes: activate tkinter.Tk.destroy()
        """

    def __init__(self):
        """
        Window Class constructor to initialize objects

        Attributes:
            self.title: str
                        title of window
            self.geometry: str
                           window size
            self.text: tk.Text
                       places path to window
            self.new_file: str
                           contains path
        Widgets:
            path_txt: tkinter.Label
                      Used for print chosen path
            op_label: tkinter.Label
                      Label before operation choose
            func_box: tkinter.ttk.Combobox
                      Used for choose function
            file_button: tkinter.Button
                         Used for path choose
            next_button: tkinter.Button
                         Used for opening sub-window with function params
            quit_button: tkinter.Button
                         Quit button
        """
        super().__init__()

        """ Window params: """
        self.title('JSON to EXCEL')
        self.geometry('600x100')

        """ Attributes: """
        self.text = tk.Text(self, height=10, width=50)
        self.new_file = None

        """ Widgets: """
        self.path_txt = tk.Label(self)
        self.path_txt.grid(column=4, row=1)

        self.op_label = tk.Label(text="Choose an operation: ",
                                 font=('Arial', 9))
        self.op_label.grid(column=0, row=1, padx=10)

        self.func_box = Combobox(self, state='readonly')
        self.func_box['values'] = keys_list
        self.func_box.current(0)
        self.func_box.grid(column=1, row=1, padx=10)

        self.file_button = tk.Button(self, text="Choose file",
                                     command=self.save_file)
        self.file_button.grid(column=3, row=1, padx=20)

        self.next_button = tk.Button(self, text='Next', command=self.start)
        self.next_button.grid(column=3, row=2)

        self.quit_button = tk.Button(self, text='Quit', command=self.destroy)
        self.quit_button.grid(column=0, row=2)

    def save_file(self):
        """
        Starts filedialog, reformat received string into path,
        changes self.path_txt and self.new_file
        """
        self.new_file = filedialog.asksaveasfile(title="Save file",
                                                 defaultextension=".xlsx",
                                                 filetypes=(
                                                     ("Excel files", ".xlsx"),
                                                     ("all files", "*.*"))
                                                 )
        if self.new_file:
            string = str(self.new_file)
            string = string.replace("<_io.TextIOWrapper name='", '')
            del_index = string.index("' mode")
            string = string[0:del_index]
            self.path_txt.configure(text=string)
            self.new_file = string

    @exception
    def start(self):
        """
        Opens sub-window with function and give func name with path
        If self.new_file is None: raise FileNotFoundError
        """
        if self.new_file is None:
            msgbox.showerror("ERROR", 'Filepath is not specified')
            raise FileNotFoundError('Filepath is not specified')
        elif self.func_box.get() == 'orders':
            wind = Orders(self.func_box.get(), self.new_file)
            wind.mainloop()
        elif self.func_box.get() == 'stocks':
            wind = Stocks(self.func_box.get(), self.new_file)
            wind.mainloop()

    def destroy(self):
        """
        Overrides method tkinter.Tk.destroy()
        Open sub-window with ask of exit.
        If yes: activate tkinter.Tk.destroy()
        """
        if msgbox.askokcancel("Close app?", "Would you like to close an app?"):
            tk.Tk.destroy(self)
        else:
            pass


class CalendarDialog(tk.Toplevel):
    """
    Class used to start dialog with date choosing. Inherit tk.Toplevel.

    Attributes:
        self.title: str
                    Window title
        result: datetime obj
                Date, chosen by user
    Widgets:
        calendar: tkcalendar.Calendar
                  Calendar gui, if date chosen: configure date_label
        ok_button: tkinter.Button
                   On press start ok_and_exit method,
                   which get chosen date and close window
        date_label: tkinter.Label
                    Label with chosen date, changes by calendar.bind()
    Attributes:
        result: datetime.date obj
    Methods:
        __init__(self): Initialize attributes and widgets
        check_date(self, event): Started when chose date. Change date_label
        ok_and_exit(self): Get selected date from calendar and return it
                           with closing a window
    """
    def __init__(self):
        """
        CalendarDialog Class constructor to initialize objects

        Attributes:
            self.title: str
                   Window title
            self.result: datetime obj
                    Date, chosen by user
        Widgets:
            calendar: tkcalendar.Calendar
                      Calendar gui, if date chosen: configure date_label
            ok_button: tkinter.Button
                       On press start ok_and_exit method,
                       which get chosen date and close window
            date_label: tkinter.Label
                        Label with chosen date, changes by calendar.bind()
        """
        super().__init__()

        """ Window params"""
        self.title("Choose date")

        """ Widgets: """
        self.calendar = Calendar(self, selectmode='day')
        self.calendar.grid(column=1, row=0)
        self.calendar.bind('<<CalendarSelected>>', self.check_date)

        self.date_label = tk.Label(self, text="")
        self.date_label.grid(column=1, row=1)
        self.date_label.config(text=f"Selected Date is:"
                                    f"{self.calendar.get_date()}")

        self.ok_button = tk.Button(self,
                                   text='Ok and exit',
                                   command=self.ok_and_exit)
        self.ok_button.grid(column=1, row=2)

        """ Attributes: """
        self.result = self.calendar.selection_get()

    def check_date(self, event):
        """
        Started when chose date. Change date_label

        :param event: str, event
        :type event: tcl.event
        """
        self.date_label.config(text=f"Selected Date is: \
                                    {self.calendar.get_date()}")

    def ok_and_exit(self):
        """
        Get selected date from calendar and return it with closing a window

        :return: date, activate self.destroy()
        :rtype: date obj
        """
        self.result = self.calendar.selection_get()
        return self.result, self.destroy()


class Widgets(tk.Toplevel):
    """
    Sub-window parent class with parameters labels of func
    Inherit: tk.Toplevel, Heirs: Orders, Stocks, Cost

    Attributes:
        key: str
               name of function
        path: str
              path to save file
        param_dict: dict
              dict with parameters of function
    Widgets:
        cancel_button: tkinter.Button
                       Button for cancel
        start_button: tkinter.Button
                      Button for start
        valid_num_command: tkinter.register
                           Entry validator for int
        label_text: tk.Label
                    Labels with name of function params
    Methods:
        __init__(self): Initialize attributes and widgets
        param_checker(self): Checks some of the function params
                             from param_dict
                             :return: True or rise exception
        only_num(self, take): method for validator, check input
                              chars on digit or not
        cancel(self): Opens ask window, if yes - close window
        start_convert(self): Opens sub-window with function params and
                             raise PermissionError
                             Function must be overridden by heirs

        saving(self): creates Getters and Converter objects, that save
                      result of request on path.
                      Then ask in ask window about same function
                      with another params
    """
    def __init__(self, key, path):
        """
        Initialize attributes and widgets

        Attributes:
            Taken:
            :param key: name of function
            :type key: str
            :param path: path to save file
            :type path: str
            Not taken:
            param_dict: dict with parameters of function
            param_dict: dict

        Widgets:
            cancel_button: tkinter.Button
                           Button for cancel
            start_button: tkinter.Button
                          Button for start
            valid_num_command: tkinter.register
                               Entry validator for int
            label_text: tk.Label
                        Labels with name of function params
        """
        super().__init__()
        self.key = key
        self.path = path
        self.param_dict = {}

        self.cancel_button = tk.Button(self,
                                       text='Cancel',
                                       command=self.cancel)
        self.cancel_button.grid(column=0, row=4)

        self.start_button = tk.Button(self,
                                      text='Start',
                                      command=self.start_convert)
        self.start_button.grid(column=3, row=4)

        self.valid_num_command = self.register(self.only_num)

        # Next code parses by PARAMS dict to place labels
        row = 0
        column = 0
        for element in PARAMS[self.key]:
            element_key = element
            if isinstance(element, dict):
                element_key = list(element.keys())[0]
            label_text = element_key.replace('_', ' ')
            label_text[0].upper()
            new_label = tk.Label(self, text=label_text)
            new_label.grid(column=column, row=row)
            row += 1
            if row > 2:
                row = 0
                column += 2

    @exception
    def param_checker(self):
        """
        Checks some of the function params from param_dict

        :return: True or rise exception
        :rtype: Boolean or Exception
        """
        keys = list(self.param_dict.keys())
        take_skip_differ = (int(self.param_dict['take']) -
                            int(self.param_dict['skip']))
        if 'date_start' in keys and 'date_end' in keys:
            date_start = self.param_dict['date_start']
            date_end = self.param_dict['date_end']
            if date_start > date_end:
                msgbox.showerror("Date Differ error",
                                 "Date start must be earlier, then date end")
                raise errors.DateDifferError()

        if 1 > take_skip_differ or take_skip_differ > 1000:
            msgbox.showerror(
                'Take And Skip differ error',
                'Differ between take and skip must be between 1000 and 0')
            raise errors.TakeAndSkipDifferError(self.param_dict['take'],
                                                self.param_dict['skip'])
        return True

    @exception
    def only_num(self, take):
        """
        Method for validator, check input chars, if digit - return True
        :param take: string from tk.Entry
        :type take: str
        :return: True or UserWarning
        :rtype: Boolean or Exception
        """
        if take.isdigit():
            if int(take) >= 0:
                return True
            else:
                msgbox.showerror('Input error',
                                 'Digit must be more or equal than 0')
                raise UserWarning('Try to input "-" digit')
        else:
            msgbox.showerror("Input Error", "Only digits here")
            raise UserWarning("Try to input char in field take or skip")

    def cancel(self):
        """
        Opens ask window, if yes - close window
        """
        if msgbox.askokcancel('Close window?', 'Close window?'):
            self.destroy()
        else:
            pass

    @exception
    def start_convert(self):
        """
        Opens sub-window with function params and raise PermissionError
        Function must be overridden by heirs
        :raise: PermissionError
        """
        msgbox.showerror("Start",
                         f"Starting with params: \n"
                         f"{self.param_dict} \n Func must be reassigned!")
        raise PermissionError('Func must be reassigned')

    @exception
    def saving(self):
        """
        Creates Getters and Converter objects, that save
        result of request on path.
        Then ask in ask window about same function with another params
        """

        request = logic.Getters(self.key, self.param_dict)
        try:
            my_json = request.response()
        except requests.exceptions.ConnectionError:
            msgbox.showerror("Connection error",
                             "Unable to connect with Wildberries. \n"
                             "Check your network")
            raise requests.exceptions.ConnectionError
        try:
            logic.Converter(self.path, self.key, my_json).convert()
        except AttributeError:
            msgbox.showerror('Error from server.',
                             'Error from server, check logs')
            raise AttributeError
        except ValueError:
            msgbox.showerror('Data is none',
                             'Get empty data from server\n'
                             'Try change request')
            raise ValueError
        question = msgbox.askquestion("Another request?",
                                      "Want you create order request"
                                      "with another params?")
        if question == 'yes':
            save_wind = Window()
            save_wind.save_file()
            pass
        else:
            self.destroy()


class Orders(Widgets):
    """
    Sub-window class for getting 'order' function request with params
    and saving it
    Inherit: Widgets

    Attributes:
        key: str
             name of function
        path: str
              path to save file
        self.param_dict: dict
                         dict with parameters of function
    Widgets:
        calendar_start_butt: tkinter.Button
                             Button for open date-choose window
        calendar_end_butt: tkinter.Button
                           Button for open date-choose window
        status_box: tkinter.ttk.Combobox
                    Combobox with 'status' parameter values
        take_num: tkinter.Entry
                  Entry to the int, 'take' parameter
        skip_num: tkinter.Entry
                  Entry to the int, 'take' parameter
        id_num: tkinter.Entry
                Entry to the int, 'take' parameter
    Methods:
        __init__(self): Initialize attributes and widgets
        get_date(self, key): Open sub-window with date choose, then check it
        start_convert(self): Function overridden from Widgets.
                             Get params from widgets and pack into dict
                             After run Widgets.save(self)
    """

    STATUSES_LIST = [0, 1, 2, 3, 5, 6, 7]  # List for status_box

    def __init__(self, key, path):
        """
        Attributes:
            Taken:
            :param key: name of function
            :type key: str
            :param path: path to save file
            :type path: str
            Not taken:
            param_dict: dict with parameters of function
            param_dict: dict
        Widgets:
            calendar_start_butt: tkinter.Button
                                 Button for open date-choose window
            calendar_end_butt: tkinter.Button
                               Button for open date-choose window
            status_box: tkinter.ttk.Combobox
                        Combobox with 'status' parameter values
            take_num: tkinter.Entry
                      Entry to the int, 'take' parameter
            skip_num: tkinter.Entry
                      Entry to the int, 'take' parameter
            id_num: tkinter.Entry
                    Entry to the int, 'take' parameter
        """
        super().__init__(key, path)

        """ Widgets: """
        self.calendar_start_butt = tk.Button(
                                   self, text='Choose date',
                                   command=lambda: self.get_date('date_start')
                                   )
        self.calendar_start_butt.grid(column=1, row=0)

        self.calendar_end_butt = tk.Button(
                                 self, text='Choose date',
                                 command=lambda: self.get_date('date_end')
                                 )
        self.calendar_end_butt.grid(column=1, row=1)

        self.status_box = Combobox(self, state='readonly')
        self.status_box['values'] = Orders.STATUSES_LIST
        self.status_box.grid(column=1, row=2)

        self.take_num = tk.Entry(self, validate='key',
                                 validatecommand=(self.valid_num_command, '%S')
                                 )
        self.take_num.grid(column=3, row=0)
        self.take_num.insert(0, 1000)

        self.skip_num = tk.Entry(self, validate='key',
                                 validatecommand=(self.valid_num_command, '%S')
                                 )
        self.skip_num.grid(column=3, row=1)
        self.skip_num.insert(0, 0)

        self.id_num = tk.Entry(self, validate='key',
                               validatecommand=(self.valid_num_command, '%S'))
        self.id_num.grid(column=3, row=2)

    @exception
    def get_date(self, key):
        """
        Open sub-window with date choose, then check it
        :param key: key to check date
        :type key: str
        :raise: errors.StartDateAttributeError
        """
        calendar = CalendarDialog()
        self.wait_window(calendar)
        result = calendar.result
        if key == 'date_start':
            if result > datetime.date.today():
                msgbox.showerror("Date error",
                                 "Start date must be today or earlier")
                raise errors.StartDateAttributeError(result)
        self.param_dict[key] = result

    def start_convert(self):
        """
        Function overridden from Widgets.
        Get params from widgets and pack into dict
        After run Widgets.save(self)
        """
        if self.status_box.get() != '':
            self.param_dict['status'] = self.status_box.get()
        else:
            self.param_dict['status'] = None
        if self.take_num.get() != '':
            self.param_dict['take'] = self.take_num.get()
        if self.skip_num.get() != '':
            self.param_dict['skip'] = self.skip_num.get()
        if self.id_num.get() != '':
            self.param_dict['order_id'] = self.id_num.get()
        if Widgets.param_checker(self):
            Widgets.saving(self)


class Stocks(Widgets):
    """
    Sub-window class for getting 'stocks' function request with params
    and saving it
    Inherit: Widgets

    Attributes:
        key: str
             name of function
        path: str
              path to save file
        self.param_dict: dict
                         dict with parameters of function
    Widgets:
        search: tkinter.Entry
                Entry for all chars
        take_num: tkinter.Entry
                  Entry to the int, 'take' parameter
        skip_num: tkinter.Entry
                  Entry to the int, 'take' parameter
        sort_box: tkinter.ttk.Combobox
                    Combobox with 'sort' parameter values
        order_box: tkinter.ttk.Combobox
                    Combobox with 'order' parameter values
    Methods:
        __init__(self): Initialize attributes and widgets
        start_convert(self): Function overridden from Widgets.
                             Get params from widgets and pack into dict
                             After run Widgets.save(self)
    """
    def __init__(self, key, path):
        """
        Initialize attributes and widgets
        Attributes:
            key: str
                 name of function
            path: str
                  path to save file
            self.param_dict: dict
                             dict with parameters of function
        Widgets:
            search: tkinter.Entry
                    Entry for all chars
            take_num: tkinter.Entry
                      Entry to the int, 'take' parameter
            skip_num: tkinter.Entry
                      Entry to the int, 'take' parameter
            sort_box: tkinter.ttk.Combobox
                      Combobox with 'sort' parameter values
            order_box: tkinter.ttk.Combobox
                       Combobox with 'order' parameter values
        """
        super().__init__(key, path)

        """ Widgets: """
        self.search = tk.Entry(self)
        self.search.grid(column=1, row=0)

        self.take_num = tk.Entry(self, validate='key',
                                 validatecommand=(self.valid_num_command, '%S')
                                 )
        self.take_num.grid(column=1, row=1)
        self.take_num.insert(0, 1000)

        self.skip_num = tk.Entry(self, validate='key',
                                 validatecommand=(self.valid_num_command, '%S')
                                 )
        self.skip_num.grid(column=1, row=2)
        self.skip_num.insert(0, 0)

        self.sort_box = Combobox(self, state='readonly')
        self.sort_box['values'] = logic.RIGHT_SORT_LIST
        self.sort_box.grid(column=3, row=0)

        self.order_box = Combobox(self, state='readonly')
        self.order_box['values'] = logic.ORDER_LIST
        self.order_box.current(0)
        self.order_box.grid(column=3, row=1)

    def start_convert(self):
        """
        Function overridden from Widgets.
        Get params from widgets and pack into dict
        After run Widgets.save(self)
        """
        if self.search != '':
            self.param_dict['search'] = self.search.get()
        if self.take_num.get() != '':
            self.param_dict['take'] = self.take_num.get()
        if self.skip_num.get() != '':
            self.param_dict['skip'] = self.skip_num.get()
        if self.sort_box.get() != '':
            self.param_dict['sort'] = self.sort_box.get()
        else:
            self.param_dict['sort'] = None
        if self.order_box.get() != '':
            self.param_dict['order'] = self.order_box.get()
        else:
            self.param_dict['order'] = 'asc'
        if Widgets.param_checker(self):
            Widgets.saving(self)


class Costs(Widgets):
    """
    Sub-window class for getting 'costs' function request with params
    and saving it
    Inherit: Widgets

    Attributes:
        key: str
             name of function
        path: str
              path to save file
        self.param_dict: dict
                         dict with parameters of function
    Widgets:
        quantity_box: tkinter.ttk.Combobox
                    Combobox with 'quantity' parameter values
    Methods:
        __init__(self): Initialize attributes and widgets
        start_convert(self): Function overridden from Widgets.
                             Get params from widgets and pack into dict
                             After run Widgets.save(self)
    """
    
    #  Values list for self.quantity_box
    QUANTITY_LIST = [1, 2, 0]

    def __init__(self, key, path):
        super().__init__(key, path)

        """ Widgets: """
        self.quantity_box = Combobox(self, state='readonly')
        self.quantity_box['values'] = self.QUANTITY_LIST
        self.quantity_box.current(0)
        self.quantity_box.grid(column=1, row=0)

    def start_convert(self):
        self.param_dict['quantity'] = self.quantity_box.get()
        if Widgets.param_checker(self):
            Widgets.saving(self)
