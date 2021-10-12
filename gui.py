import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkcalendar import DateEntry

params = {
        'orders': ['date_start', 'date_end', 'status', 'take', 'skip', 'order_id'],
        'warehouses': None,
        'costs': ['quantity'],
        'stocks': ['search', 'sort', 'order'],
        'config': ['name'],
        'search by pattern': ['name', 'parent', 'lang'],
        'tnved': ['obj_id', 'subject', 'pattern'],
        'list': [],
        'other': ['top', 'pattern', 'id']
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
        else:
            wind = Widgets(self.func_box.get(), self.new_file)
            wind.mainloop()

    def exit(self):
        if msgbox.askokcancel("Close app?", "Would you like to close an app?"):
            self.destroy()
        else:
            pass


class Widgets(tk.Toplevel):
    def __init__(self, key, path):
        super().__init__()
        self.key = key
        self.path = path
        self.param_dict = {}
        self.labels = Widgets.label_func(self)

        self.goodbye_button = tk.Button(self, text='Cancel', command=self.cancel)
        self.goodbye_button.grid(column=0, row=4)

        self.start_button = tk.Button(self, text='Start', command=self.start_convert)
        self.start_button.grid(column=3, row=4)

    def label_func(self):
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

    def create_fields(self):
        if self.key == 'orders':
            self.calendar_start_butt = tk.Button(self, text='Choose date', command=lambda: self.get_date('date_start'))
            self.calendar_start_butt.grid(column=1, row=0)
            self.calendar_end_butt = tk.Button(self, text='Choose date', command=lambda: self.get_date('date_end'))
            self.calendar_end_butt.grid(column=1, row=1)
            self.new_box = Combobox(self)
            self.new_box['values'] = params[self.key][2]['status']
            self.new_box.current(0)
            self.new_box.grid(column=1, row=2)
            return self.calendar_start_butt, self.calendar_end_butt, self.new_box


    def cancel(self):
        if msgbox.askokcancel('Close window?', 'Close window?'):
            self.destroy()
        else:
            pass

    def get_date(self, key):
        cal_widget = DateEntry()
        cal_widget.drop_down()
        date = cal_widget.get_date()
        self.param_dict[key] = date
        print(self.param_dict)

    def start_convert(self):
        print(self.param_dict)
        msgbox.showinfo("I'm starting with params: \n", self.param_dict)


