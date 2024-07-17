from tkinter import *
from tkinter import colorchooser, filedialog
from tkinter import ttk
import pyperclip
import vehicle
import instrument
from window_exit import Window_Exit
from PIL import Image, ImageTk, ImageGrab
from calculator import Distant_Calculate


MAIN_BG = '#71bd6f'
MAIN_FG = '#ffffff'

CURSORS = {
    'brush': 'arrow',
    'eraser': 'dotBox',
    'oval': 'circle',
    'rectangle': 'sizing',
    'line': 'draft_small',
    'grab': 'fleur',
    'text': 'xterm',
    'arrow': 'top_right_corner'
}

BUTTON_IMAGE_PATH = {
    'brush': 'image_tool/brush.png',
    'eraser': 'image_tool/eraser.png',
    'oval': 'image_tool/oval.png',
    'rectangle': 'image_tool/rectangle.png',
    'line': 'image_tool/line.png',
    'arrow': 'image_tool/arrow.png',
    'grab': 'image_tool/grab.png',
}

MUSHROOM_PATH = {
    'basket': 'image/basket.png',
    'gruzd': 'image/gruzd.png',
    'podberezovik': 'image/podberezovik.png',
    'podosinovik': 'image/podosinovik.png',
    'rizhik': 'image/rizhik.png',
    'muhomor': 'image/muhomor.png'
}

SET_TOOL = {'oval', 'rectangle', 'line', 'arrow'}


class Window:

    def __init__(self, width=1280, height=720, resizable=(False, False),
                 fullscreen=False, title='Виртуальная доска', icon=None):
        self.link_icon = icon
        self.root = Tk()
        self.root.attributes('-fullscreen', fullscreen)
        self.root.configure(bg=MAIN_BG)
        width_canvas = self.root.winfo_screenwidth() - 80
        height_canvas = self.root.winfo_screenheight() - 80
        if not fullscreen:
            self.root.geometry(f'{width}x{height}')
            self.root.resizable(resizable[0], resizable[1])
            width_canvas = width - 80
            height_canvas = height - 80
            if icon:
                self.root.iconbitmap(default=self.link_icon)
        self.root.title(title)

        # self.river = self.road_line = self.ship = self.ship2 = self.green_car = self.blue_car = None
        self.coefficient_time = None
        self.vehicle = None
        self.picture = None
        self.canvas = Canvas(self.root, width=width_canvas, height=height_canvas)
        self.bg = PhotoImage(file='image/cell.png')
        self.bg_id = self.canvas.create_image(0, 0, anchor=NW, image=self.bg, tags='background')
        self.tool = 'brush'
        self.change_tool(self.tool)
        self.current_color = '#000000'
        self.current_bg_color = None
        self.width_line = IntVar(value=5)
        self.switch_fill = IntVar()
        self.frame_parameter = Frame()
        self.vehicle_parameter = self.canvas.create_window(10, 10, anchor=NW, window=self.frame_parameter,
                                                           tags='vehicle_param')
        self.dict_vehicle = {}
        self.dict_image = {}
        self.dict_way = {}
        self.time_move = IntVar()
        self.tick = 0
        self.time_des = StringVar(value='секунды')

        self.canvas.bind('<ButtonPress-1>', self.set_coord)
        self.canvas.bind('<MouseWheel>', self.change_width_line)
        self.root.bind('<Control-z>', self.cancel_lust_move)
        self.root.bind('<Control-v>', self.paste_on_canvas)
        self.root.bind('<Escape>', self.create_window_exit)

        self.create_menu()

        self.frame_top = Frame(self.root, bg=MAIN_BG)
        self.lbl_time = Label(self.frame_top, text='Время:', font=('Arial', 12, 'bold'))
        self.entry_tick = ttk.Entry(self.frame_top, textvariable=self.time_move, width=5, font=('Arial', 12, 'bold'))
        self.combobox_speed = ttk.Combobox(self.frame_top, values=['часы', 'минуты', 'секунды'],
                                           width=8, font=('Arial', 12), textvariable=self.time_des)
        # self.scale_width_line = ttk.LabeledScale(self.frame_top, from_=1.0, to=30, variable=self.width_line)
        self.scale_width_line = Scale(self.frame_top, from_=1.0, to=30, variable=self.width_line,
                                      orient=HORIZONTAL, bg=MAIN_BG, fg=MAIN_FG, activebackground=MAIN_BG)
        self.btn_play = Button(self.frame_top, text='►', width=7, command=self.play_all)
        self.btn_stop_play = Button(self.frame_top, text='■', width=5, command=self.stop_play)
        self.lbl_time = Label(self.frame_top, text=0, font=('Arial', 12, 'bold'), bg=MAIN_BG, fg=MAIN_FG)

        self.frame_button = Frame(self.root)
        self.img_brush = ImageTk.PhotoImage(Image.open(BUTTON_IMAGE_PATH['brush']))
        self.img_eraser = ImageTk.PhotoImage(Image.open(BUTTON_IMAGE_PATH['eraser']))
        self.img_oval = ImageTk.PhotoImage(Image.open(BUTTON_IMAGE_PATH['oval']))
        self.img_rectangle = ImageTk.PhotoImage(Image.open(BUTTON_IMAGE_PATH['rectangle']))
        self.img_line = ImageTk.PhotoImage(Image.open(BUTTON_IMAGE_PATH['line']))
        self.img_arrow = ImageTk.PhotoImage(Image.open(BUTTON_IMAGE_PATH['arrow']))
        self.img_grab = ImageTk.PhotoImage(Image.open(BUTTON_IMAGE_PATH['grab']))
        self.btn_brush = Button(self.frame_button, image=self.img_brush, command=lambda: self.change_tool('brush'))
        self.btn_eraser = Button(self.frame_button, image=self.img_eraser, command=lambda: self.change_tool('eraser'))
        self.btn_oval = Button(self.frame_button, image=self.img_oval, command=lambda: self.change_tool('oval'))
        self.btn_rectangle = Button(self.frame_button, image=self.img_rectangle,
                                    command=lambda: self.change_tool('rectangle'))
        self.btn_line = Button(self.frame_button, image=self.img_line, command=lambda: self.change_tool('line'))
        self.btn_arrow = Button(self.frame_button, image=self.img_arrow, command=lambda: self.change_tool('arrow'))
        self.btn_text = Button(self.frame_button, text='Текст', font=('Times New Roman', 12, 'bold'),
                               command=lambda: self.change_tool('text'))
        self.btn_grab = Button(self.frame_button, image=self.img_grab, command=lambda: self.change_tool('grab'))
        self.clear_all = Button(self.frame_button, text='Очистить', font=('Times New Roman', 12), command=self.cls)
        self.btn_color = Button(self.frame_button, text='Выбрать\nцвет', font=('Times New Roman', 12), bg='black',
                                fg='white', command=self.change_color)
        self.check_btn_fill = ttk.Checkbutton(self.frame_button, text='Заливка', variable=self.switch_fill,
                                              command=self.change_bg_color)

        self.frame_close = Frame(self.root)
        self.btn_exit = Button(self.frame_close, text='X', fg='red', width=3,
                               command=lambda: self.create_window_exit(''))
        self.btn_minimize = Button(self.frame_close, text='_', width=3, command=self.root.iconify)
        self.list_move = []

        self.draw_widget()

    def cancel_lust_move(self, event):
        if self.list_move:
            for i in self.list_move[-1]:
                self.canvas.delete(i)
            del self.list_move[-1]

    def draw_widget(self):
        self.frame_close.grid(row=0, column=1)
        self.btn_minimize.grid(row=0, column=0)
        self.btn_exit.grid(row=0, column=1)

        self.frame_top.grid(row=0)
        self.lbl_time.grid(row=0, column=0)
        self.entry_tick.grid(row=0, column=1, padx=10)
        self.combobox_speed.grid(row=0, column=2)
        self.scale_width_line.grid(row=0, column=3, padx=10)
        self.btn_play.grid(row=0, column=4, padx=10)
        self.btn_stop_play.grid(row=0, column=5)
        self.lbl_time.grid(row=0, column=6, padx=10)

        self.canvas.grid(row=1, column=0)

        self.frame_button.grid(row=1, column=1)
        self.btn_brush.pack(fill=X)
        self.btn_eraser.pack(fill=X)
        self.btn_oval.pack(fill=X)
        self.btn_rectangle.pack(fill=X)
        self.btn_line.pack(fill=X)
        self.btn_arrow.pack(fill=X)
        self.btn_text.pack(fill=X)
        self.btn_grab.pack(fill=X)
        self.clear_all.pack(fill=X)
        self.btn_color.pack(fill=X)
        self.check_btn_fill.pack(fill=X)

    def create_menu(self):
        main_menu = Menu(self.root, bg='#4b964a')
        menu_add = Menu(tearoff=0, font='Arial, 12', bg='#e8fdff')
        menu_calculator = Menu(tearoff=0, font='Arial, 12', bg='#e8fdff')
        main_menu.add_cascade(label='Добавить', menu=menu_add)
        main_menu.add_cascade(label='Калькулятор', menu=menu_calculator)

        menu_add.add_command(label='Река', command=lambda: self.add_vehicle('way', 'river', 'Река'))
        menu_add.add_command(label='Дорога', command=lambda: self.add_vehicle('way', 'road_line', 'Дорога'))
        menu_add.add_separator()
        menu_add.add_command(label='Оранжевая лодка',
                             command=lambda: self.add_vehicle('vehicle', 'ship', 'Оранжевая лодка'))
        menu_add.add_command(label='Зеленая лодка',
                             command=lambda: self.add_vehicle('vehicle', 'ship2', 'Зеленая лодка'))
        menu_add.add_command(label='Синяя машина',
                             command=lambda: self.add_vehicle('vehicle', 'blue_car', 'Синяя машина'))
        menu_add.add_command(label='Зеленая машина',
                             command=lambda: self.add_vehicle('vehicle', 'green_car', 'Зеленая машина'))
        menu_add.add_separator()
        menu_mushroom = Menu(tearoff=0, bg='#e8fdff')
        menu_mushroom.add_command(label='Корзинка', command=lambda: self.add_picture(MUSHROOM_PATH['basket']))
        menu_mushroom.add_command(label='Груздь', command=lambda: self.add_picture(MUSHROOM_PATH['gruzd']))
        menu_mushroom.add_command(label='Подберезовик', command=lambda: self.add_picture(MUSHROOM_PATH['podberezovik']))
        menu_mushroom.add_command(label='Подосиновик', command=lambda: self.add_picture(MUSHROOM_PATH['podosinovik']))
        menu_mushroom.add_command(label='Рыжик', command=lambda: self.add_picture(MUSHROOM_PATH['rizhik']))
        menu_mushroom.add_command(label='Мухомор', command=lambda: self.add_picture(MUSHROOM_PATH['muhomor']))
        menu_add.add_cascade(label='Грибы', menu=menu_mushroom)
        menu_add.add_separator()
        menu_add.add_command(label='Изображение', command=self.get_picture_path)

        menu_calculator.add_command(label='Движение', command=lambda: Distant_Calculate(parent=self,
                                                                                        icon=self.link_icon))

        self.root.config(menu=main_menu)

    def add_vehicle(self, tag, tag_name, title):
        if tag == 'way':
            self.vehicle = vehicle.Way(parent=window, tag=tag, tag_name=tag_name, title=title)
            self.dict_way[self.vehicle.picture_id] = self.vehicle
        elif tag == 'vehicle':
            self.vehicle = vehicle.Vehicle(parent=window, tag=tag, tag_name=tag_name, title=title)
            self.dict_vehicle[self.vehicle.picture_id] = self.vehicle

    def get_picture_path(self):
        image_path = filedialog.askopenfilename()
        self.add_picture(image_path)

    def add_picture(self, path):
        self.picture = ImageTk.PhotoImage(Image.open(path))
        self.dict_image[self.canvas.create_image(10, 10, anchor=NW, image=self.picture, tags='image')] = self.picture

    def paste_on_canvas(self, event):
        paste_text = pyperclip.paste()
        if str(self.root.focus_get()) == '.':
            if paste_text:
                self.canvas.create_text(50, 50, text=paste_text,
                                        font=('Arial', self.width_line.get() * 3),
                                        fill=self.current_color,
                                        anchor=NW, width=1200)
            elif ImageGrab.grabclipboard():
                if type(ImageGrab.grabclipboard()) is list:
                    self.add_picture(ImageGrab.grabclipboard()[0])
                else:
                    self.picture = ImageTk.PhotoImage(ImageGrab.grabclipboard())
                    self.dict_image[self.canvas.create_image(10, 10, anchor=NW,
                                                             image=self.picture,
                                                             tags='image')] = self.picture

    def add_text(self, x, y):
        frame_text = Frame()
        Text(frame_text, fg=self.current_color, bg=self.current_bg_color,
             relief=RIDGE, borderwidth=self.width_line.get() * 1.5, width=25, height=3,
             font=('Arial', self.width_line.get() * 3), wrap='word').pack()
        # Label(frame_text, text='==', height=1).pack()
        self.canvas.create_window(x, y, anchor=NW, window=frame_text, tags='text')

    def play_all(self):
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
        # self.coefficient_time = 100 / self.tick
        # self.tick = 100
        list_keys = list(self.dict_way.keys())
        for item in list_keys:
            self.dict_way[item].assign_parameter(self.coefficient_time)
        list_keys = list(self.dict_vehicle.keys())
        for item in list_keys:
            self.dict_vehicle[item].assign_parameter(self.coefficient_time)

        self.motion()

    def motion(self):
        if self.tick > 0:
            for item in self.dict_vehicle:
                self.dict_vehicle[item].move_vehicle()
            self.tick -= 1
            if self.time_des.get() == 'минуты':
                self.lbl_time.config(text=f'{int(self.time_move.get() - self.tick / self.coefficient_time / 60)} мин.')
            elif self.time_des.get() == 'часы':
                self.lbl_time.config(text=f'{int(self.time_move.get() - self.tick / self.coefficient_time / 3600)} ч.')
            else:
                self.lbl_time.config(text=f'{int(self.time_move.get() - self.tick / self.coefficient_time)} сек.')
            self.root.after(20, self.motion)

    def stop_play(self):
        self.tick = 0

    def change_tool(self, tool):
        self.tool = tool
        self.canvas.configure(cursor=CURSORS[tool])

    def change_width_line(self, event):
        if event.delta > 0 and self.width_line.get() < 30:
            self.width_line.set(self.width_line.get() + 1)
        elif event.delta < 0 and self.width_line.get() > 1:
            self.width_line.set(self.width_line.get() - 1)

    def set_coord(self, event):
        self.root.focus_set()
        if self.tool == 'brush':
            instrument.Curve(parent=window, x=event.x, y=event.y)
        elif self.tool == 'eraser':
            instrument.Eraser(parent=window)
        elif self.tool in SET_TOOL:
            instrument.Create_Figure(parent=window, x=event.x, y=event.y, figure=self.tool)
        elif self.tool == 'grab':
            instrument.Grab(parent=window, item=self.canvas.find_withtag(CURRENT), x=event.x, y=event.y)
        elif self.tool == 'text':
            self.add_text(x=event.x, y=event.y)

    def cls(self):
        self.canvas.delete(ALL)
        self.bg_id = self.canvas.create_image(0, 0, anchor=NW, image=self.bg, tags='background')
        self.frame_parameter.destroy()
        self.frame_parameter = Frame()
        self.vehicle_parameter = self.canvas.create_window(10, 10, anchor=NW, window=self.frame_parameter,
                                                           tags='vehicle_param')
        self.dict_way = {}
        self.dict_vehicle = {}

    def change_color(self):
        rgb_color, self.current_color = colorchooser.askcolor()
        btn_fg_color = '#' + ''.join(f'{255 - i:02x}' for i in reversed(rgb_color))
        self.btn_color.config(bg=self.current_color, fg=btn_fg_color)

    def change_bg_color(self):
        if self.switch_fill.get() == 1:
            self.current_bg_color = colorchooser.askcolor()[1]
        else:
            self.current_bg_color = None

    def run(self):
        self.root.mainloop()

    def create_window_exit(self, event):
        Window_Exit(parent=self, icon=self.link_icon)

    def exit(self):
        self.root.destroy()


if __name__ == '__main__':
    window = Window(width=1280,
                    height=720,
                    fullscreen=True,
                    icon='image/icon.ico')
    window.run()
