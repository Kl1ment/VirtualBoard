from tkinter import *
from tkinter import ttk


class Distant_Calculate:

    def __init__(self, parent, icon):
        self.root = Toplevel(parent.root)
        if icon:
            self.root.iconbitmap(default=icon)
        self.root.attributes('-topmost', True, '-toolwindow', True)
        self.root.resizable(False, False)
        self.root.title('Калькулятор движения')

        self.main_font = ('Arial', 12)
        self.frame = Frame(self.root)
        self.speed = StringVar(value='')
        self.time = StringVar(value='')
        self.distant = StringVar(value='')
        self.speed_des = StringVar(value='м/с')
        self.time_des = StringVar(value='секунды')
        self.distant_des = StringVar(value='метры')

        self.frame.pack()
        Label(self.frame, text='Скорость:', font=self.main_font).grid(row=0, column=0, sticky=E)
        Label(self.frame, text='Время:', font=self.main_font).grid(row=1, column=0, sticky=E)
        Label(self.frame, text='Расстояние:', font=self.main_font).grid(row=2, column=0, sticky=E)

        Entry(self.frame, textvariable=self.speed, font=self.main_font, width=8).grid(row=0, column=1, pady=5)
        Entry(self.frame, textvariable=self.time, font=self.main_font, width=8).grid(row=1, column=1, pady=5)
        Entry(self.frame, textvariable=self.distant, font=self.main_font, width=8).grid(row=2, column=1, pady=5)

        ttk.Combobox(self.frame, textvariable=self.speed_des,
                     values=['м/с', 'км/ч'], font=self.main_font,
                     width=10).grid(row=0, column=2)
        ttk.Combobox(self.frame, textvariable=self.time_des,
                     values=['секунды', 'минуты', 'часы'], font=self.main_font,
                     width=10).grid(row=1, column=2)
        ttk.Combobox(self.frame, textvariable=self.distant_des,
                     values=['метры', 'километры'], font=self.main_font,
                     width=10).grid(row=2, column=2)
        Button(self.frame, text='Рассчитать',
               font=self.main_font, command=self.calculate).grid(row=3, column=0, columnspan=3)
        self.lbl_result = Label(self.frame, font=('Arial', 12))
        self.lbl_result.grid(row=4, columnspan=3)

    def calculate(self):
        res = ''

        def trans_speed(from_: str, to_: str, speed_value: float) -> (float, str):
            if from_ == 'км/ч' and to_ == 'м/с':
                return speed_value / 3.6, f'{speed_value} км/ч : 3.6 = {speed_value / 3.6} м/с\n'
            elif from_ == 'м/с' and to_ == 'км/ч':
                return speed_value * 3.6, f'{speed_value} м/с * 3.6 = {speed_value * 3.6} км/ч\n'
            return speed_value, ''

        def trans_distant(from_: str, to_: str, distant_value: float) -> (float, str):
            if from_ == 'километры' and to_ == 'метры':
                return distant_value * 1000, f'{distant_value} км. * 1000 = {distant_value * 1000} м\n'
            elif from_ == 'метры' and to_ == 'километры':
                return distant_value / 1000, f'{distant_value} м. : 1000 = {distant_value / 1000} км\n'
            return distant_value, ''

        def trans_time(from_: str, to_: str, time_value: float) -> (float, str):
            if from_ == 'часы' and to_ == 'секунды':
                return time_value * 3600, f'{time_value} ч. * 3600 = {time_value * 3600} сек\n'
            elif from_ == 'минуты' and to_ == 'секунды':
                return time_value * 60, f'{time_value} мин. * 60 = {time_value * 60} сек\n'
            elif from_ == 'секунды' and to_ == 'часы':
                return time_value / 3600, f'{time_value / 3600} сек. : 3600 = {time_value} ч\n'
            elif from_ == 'минуты' and to_ == 'часы':
                return time_value / 60, f'{time_value} мин. : 60 = {time_value} ч\n'
            return time_value, ''

        if any(i.get() != '?' and not i.get().replace('.', '', 1).isdigit() for i in (self.speed,
                                                                                      self.time,
                                                                                      self.distant)):
            res += 'Некорректные данные'
        elif (self.speed.get(), self.time.get(), self.distant.get()).count('?') > 1:
            res += 'Недостаточно данных'
        elif self.speed.get() == '?':
            if self.speed_des.get() == 'м/с':
                distant, st = trans_distant(self.distant_des.get(), 'метры', float(self.distant.get()))
                res += st
                time, st = trans_time(self.time_des.get(), 'секунды', float(self.time.get()))
                res += st
                res += f'V = {distant} м. : {time} сек. = {round(distant / time, 3)} м/с'

            elif self.speed_des.get() == 'км/ч':
                distant, st = trans_distant(self.distant_des.get(), 'километры', float(self.distant.get()))
                res += st
                time, st = trans_time(self.time_des.get(), 'часы', float(self.time.get()))
                res += st
                res += f'V = {distant} км. : {time} ч. = {round(distant / time, 3)} км/ч'

        elif self.distant.get() == '?':
            if self.distant_des.get() == 'метры':
                speed, st = trans_speed(self.speed_des.get(), 'м/с', float(self.speed.get()))
                res += st
                time, st = trans_time(self.time_des.get(), 'секунды', float(self.time.get()))
                res += st
                res += f'S = {speed} м/с * {time} сек. = {speed * time} м'

            elif self.distant_des.get() == 'километры':
                speed, st = trans_speed(self.speed_des.get(), 'км/ч', float(self.speed.get()))
                res += st
                time, st = trans_time(self.time_des.get(), 'часы', float(self.time.get()))
                res += st
                res += f'S = {speed} км/ч * {time} ч. = {speed * time} км'

        elif self.time.get() == '?':
            if self.time_des.get() == 'часы':
                speed, st = trans_speed(self.speed_des.get(), 'км/ч', float(self.speed.get()))
                res += st
                distant, st = trans_distant(self.distant_des.get(), 'километры', float(self.distant.get()))
                res += st
                res += f't = {distant} км. : {speed} км/ч = {round(distant/speed, 3)} ч'
            if self.time_des.get() == 'секунды':
                speed, st = trans_speed(self.speed_des.get(), 'м/с', float(self.speed.get()))
                res += st
                distant, st = trans_distant(self.distant_des.get(), 'метры', float(self.distant.get()))
                res += st
                res += f't = {distant} м. : {speed} м/с = {round(distant/speed, 3)} сек'
            if self.time_des.get() == 'минуты':
                speed, st = trans_speed(self.speed_des.get(), 'м/с', float(self.speed.get()))
                res += st
                distant, st = trans_distant(self.distant_des.get(), 'метры', float(self.distant.get()))
                res += st
                res += f't = {distant} м. : {speed} м/с = {round(distant/speed, 3)} с\n'
                res += f'{round(distant/speed, 3)} сек. : 60 = {round(distant/speed/60, 3)} мин\n'

        else:
            speed = trans_speed(self.speed_des.get(), 'м/с', float(self.speed.get()))[0]
            time = trans_time(self.time_des.get(), 'секунды', float(self.time.get()))[0]
            distant = trans_distant(self.distant_des.get(), 'метры', float(self.distant.get()))[0]
            if round(speed * time, 2) == round(distant, 2):
                res += 'Верно'
            else:
                res += 'Неверно'

        self.lbl_result.configure(text=res)
