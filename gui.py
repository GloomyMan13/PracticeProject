import os.path as path
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter.ttk import Combobox
from tkinter import filedialog
import logic

keys_list = list(logic.KEYS.keys())


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('MyApp')
        self.geometry('600x500')
        self.text = tk.Text(self, height=10, width=50)
        self.new_file = None
        label_text = tk.StringVar()
        label_text.set('Choose operation:')


        label = tk.Label(textvar=label_text, font=('Arial', 9))
        label.grid(column=0, row=1, padx=10)

        box = Combobox()
        box['values'] = keys_list
        box.current(0)
        box.grid(column=1, row=1, padx=10)
        box.bind(0, Widgets)

        file_button = tk.Button(self, text="Choose file", command=self.save_file)
        file_button.grid(column=3, row=1, padx=20)
        reg = tk.Entry().register(Window.__changer_check)

        self.path_txt = tk.Entry(self)
        self.path_txt.grid(column=4, row=1)
        self.path_txt.configure(validate='key', validatecommand=reg)


        hello_button = tk.Button(self, text='Start', command=self.start)
        hello_button.grid(column=4, row=2)

        goodbye_button = tk.Button(self, text='Quit', command=self.exit)
        goodbye_button.grid(column=3, row=2)

    @staticmethod
    def __changer_check(input):
        if path.isfile(input):
            return True
        else:
            return False


    def save_file(self):
        self.new_file = filedialog.asksaveasfile(title="Save file",
                                                 defaultextension=".xlsx",
                                                 filetypes=(("Excel files", ".xlsx"),
                                                            ("all files", "*.*")))
        if self.new_file:
            string = str(self.new_file).replace("<_io.TextIOWrapper name='", '')
            del_index = string.index("' mode")
            string = string[0:del_index]
            self.path_txt.delete(0, 256)
            self.path_txt.insert(0, string)
            self.new_file = self.path_txt
            self.path_txt.configure(state='readonly')
            return string

    def start(self):
        if self.new_file is None:
            msgbox.showerror("ERROR", 'Filepath is not specified')
        else:
            msgbox.showinfo('OK', 'All is ok')

    def exit(self):
        if msgbox.askokcancel("Close app?", "Would you like an app?"):
            msgbox.showinfo("Goodbye!", "Sayonara")
            self.after(2, self.destroy)
        else:
            msgbox.showinfo("Not closing", "We will stay with u")


class Widgets(tk.Tk):
    def __init__(self):
        super().__init__()
        goodbye_button = tk.Button(self, text='Quit', command=self.exit)
        goodbye_button.grid(column=2, row=2)