from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

VEHICLE_PATH = {
    'river': 'image/river.png',
    'road_line': 'image/road_line.png',
    'ship': 'image/orange_ship.png',
    'ship2': 'image/green_ship.png',
    'blue_car': 'image/blue_car.png',
    'green_car': 'image/green_car.png'
}
WIDTH_PIXEL = 1200


class Way:

    def __init__(self, parent, tag, tag_name, title):
        """
        This class create ways (road, river), also it is parent for Vehicle
        Данный класс создает пути (Дорогу, реку), также является родительским для транспортных средств
        :param parent: Parent container, in this case is main window
                        Родительский контейнер, в данном случае - основное окно
        :param tag: object class tag
                        Тег класса объекта
        :param tag_name: tag of the object name
                        Тек названия объекта
        :param title: Name of vehicle
                        Нозвание транспортого средства
        """
        self.canvas = parent.canvas
        self.parent = parent
        self.tag = tag
        self.tag_name = tag_name
        self.speed_var = IntVar()
        self.speed_des = StringVar(value='м/с')
        self.speed = None
        self.direction = 'right'

        self.image_obj = Image.open(VEHICLE_PATH[tag_name])
        self.picture = ImageTk.PhotoImage(self.image_obj)
        self.picture_id = self.canvas.create_image(300, 200, anchor=NW, image=self.picture, tags=[tag])

        self.frame = Frame(parent.frame_parameter, relief=RIDGE, borderwidth=5)
        Label(self.frame, text=f'{title}', font='Arial, 12').grid(row=0, column=0)
        Label(self.frame, text='Скорость:', font='Arial, 10').grid(row=1, column=0, sticky=E)
        ttk.Entry(self.frame, textvariable=self.speed_var,
                  font=('Arial', 12, 'bold'), width=8).grid(row=1, column=1)
        ttk.Combobox(self.frame, values=['м/с', 'км/ч'],
                     width=5, font=('Arial', 12), textvariable=self.speed_des).grid(row=1, column=2, sticky=W)

        if tag == 'way':
            self.distant = None
            self.distant_var = IntVar()
            self.distant_des = StringVar(value='метры')
            Label(self.frame, text='Длина:', font='Arial, 10').grid(row=2, column=0, sticky=E)
            ttk.Entry(self.frame, textvariable=self.distant_var,
                      font=('Arial', 12, 'bold'), width=8).grid(row=2, column=1)
            ttk.Combobox(self.frame, values=['метры', 'километры'],
                         width=10, font=('Arial', 12), textvariable=self.distant_des).grid(row=2, column=2, sticky=W)
        self.frame.pack(anchor=W, pady=2)

    def assign_parameter(self, coefficient_time):
        if self.speed_des.get() == 'км/ч':
            self.speed = self.speed_var.get() / 3.6 / coefficient_time
        elif self.speed_des.get() == 'м/с':
            self.speed = self.speed_var.get() / coefficient_time

        if self.tag == 'way':
            if self.distant_des.get() == 'километры':
                self.distant = self.distant_var.get() * 1000
            elif self.distant_des.get() == 'метры':
                self.distant = self.distant_var.get()

        self.flip_left_right()

    def flip_left_right(self):
        if self.tag == 'vehicle':
            self.canvas.tag_raise(self.picture_id)
        if (self.speed >= 0) ^ (self.direction == 'right'):
            if self.direction == 'right':
                self.direction = 'left'
            else:
                self.direction = 'right'
            x, y = self.canvas.coords(self.picture_id)
            self.canvas.delete(self.picture_id)
            old_id = self.picture_id
            self.image_obj = self.image_obj.transpose(Image.FLIP_LEFT_RIGHT)
            self.picture = ImageTk.PhotoImage(self.image_obj)
            self.picture_id = self.canvas.create_image(x, y, anchor=NW,
                                                       image=self.picture, tags=[self.tag])
            if self.tag == 'way':
                self.parent.dict_way[self.picture_id] = self.parent.dict_way.pop(old_id)
            elif self.tag == 'vehicle':
                self.parent.dict_vehicle[self.picture_id] = self.parent.dict_vehicle.pop(old_id)


class Vehicle(Way):

    def __init__(self, parent, tag, tag_name, title):
        """
        This class create vehicle
        Класс создает транспортное средство
        """
        super().__init__(parent, tag, tag_name, title)
        self.tick = None
        self.coefficient_time = None
        self.x = self.picture.width() // 2
        self.y = self.picture.height()
        self.pivot = {'x': self.x, 'y': self.y}
        self.time_move = IntVar(value=0)
        self.time_des = StringVar(value='секунды')

        Button(self.frame, text='►', width=7, command=self.play_vehicle).grid(row=0, column=1)
        Button(self.frame, text='■', width=5, command=self.stop_play).grid(row=0, column=2, sticky=W)
        Label(self.frame, text='Время:').grid(row=2, column=0, sticky=E)
        ttk.Entry(self.frame, textvariable=self.time_move,
                  font=('Arial', 12, 'bold'), width=8).grid(row=2, column=1)
        ttk.Combobox(self.frame, values=['часы', 'минуты', 'секунды'],
                     width=8, font=('Arial', 12), textvariable=self.time_des).grid(row=2, column=2, sticky=W)

    def move_vehicle(self):
        self.pivot['x'] = self.canvas.coords(self.picture_id)[0] + self.x
        self.pivot['y'] = self.canvas.coords(self.picture_id)[1] + self.y
        items = self.canvas.find_overlapping(self.pivot['x'] - 1, self.pivot['y'] - 1,
                                             self.pivot['x'] + 1, self.pivot['y'] + 1)

        move = 0
        if any('way' in self.canvas.gettags(item) for item in items):
            for item in items:
                if 'way' in self.canvas.gettags(item):
                    road = self.parent.dict_way[item]
                    speed_road = WIDTH_PIXEL * road.speed / road.distant
                    speed = WIDTH_PIXEL * self.speed / road.distant
                    move = speed + speed_road
        if self.pivot['x'] + move < self.parent.root.winfo_screenwidth() - 100 and self.pivot['x'] - move > 0:
            self.canvas.move(self.picture_id, move, 0)

    def play_vehicle(self):
        if self.time_des.get() == 'минуты':
            self.tick = self.time_move.get() * 60
        elif self.time_des.get() == 'часы':
            self.tick = self.time_move.get() * 3600
        else:
            self.tick = self.time_move.get()

        if self.tick > 200:
            self.coefficient_time = 200 / self.tick
            self.tick = 200
        else:
            self.coefficient_time = 1
        # coefficient_time = 100 / self.self.parent.tick
        # self.parent.tick = 100
        dict_way_keys = list(self.parent.dict_way.keys())
        for item in dict_way_keys:
            self.parent.dict_way[item].assign_parameter(self.coefficient_time)
        self.assign_parameter(self.coefficient_time)

        self.motion()

    def motion(self):
        if self.tick > 0:
            self.move_vehicle()
            self.tick -= 1
            self.parent.root.after(20, self.motion)

    def stop_play(self):
        self.tick = 0
