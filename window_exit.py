from tkinter import *
from tkinter import ttk


class Window_Exit:

    def __init__(self, parent, width=300, height=150, resizable=(False, False), title='Выход', icon=None):
        self.root = Toplevel(parent.root)
        self.root.geometry(f'{width}x{height}+{(self.root.winfo_screenwidth()-width)//2}+{(self.root.winfo_screenheight()-height)//2}')
        self.root.resizable(resizable[0], resizable[1])
        if icon:
            self.root.iconbitmap(default=icon)
        self.root.title(title)

        self.ltl_text = ttk.Label(self.root, text='Вы действительно хотите выйти?')
        self.frame = Frame(self.root, relief=SOLID)
        self.btn_yes = ttk.Button(self.frame, text='Да', width=15, command=parent.exit)
        self.btn_no = ttk.Button(self.frame, text='Нет', width=15, command=self.exit)

        self.put_widget()
        self.grab_focus()

    def put_widget(self):
        self.ltl_text.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.frame.place(relx=0.5, rely=0.6, anchor=CENTER)
        self.btn_yes.grid(row=0, column=0, padx=5)
        self.btn_no.grid(row=0, column=1, padx=5)

    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()

    def exit(self):
        self.root.destroy()
