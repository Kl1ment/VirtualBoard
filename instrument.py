

class Curve:

    def __init__(self, parent, x, y):
        parent.list_move.append(None)
        self.parent = parent
        self.current_color = parent.current_color
        self.width_line = parent.width_line.get()
        self.parent.canvas.bind('<B1-Motion>', self.draw_curve)
        self.old_x = x
        self.old_y = y
        self.start = self.parent.canvas.find_all()[-1] + 1

    def draw_curve(self, event):
        x, y = event.x, event.y
        self.parent.list_move[-1] = range(self.start,
                                          self.parent.canvas.create_line(self.old_x, self.old_y, x, y,
                                                                         fill=self.current_color,
                                                                         width=self.width_line, capstyle='round',
                                                                         tags='curve') + 1)
        self.old_x = x
        self.old_y = y


class Eraser:

    def __init__(self, parent):
        self.parent = parent
        self.canvas = parent.canvas
        self.canvas.bind('<B1-Motion>', self.erase)

    def erase(self, event):
        items = self.canvas.find_overlapping(event.x - 10, event.y - 10, event.x + 10, event.y + 10)
        for item in items:
            if item != self.parent.bg_id and item != self.parent.vehicle_parameter:
                if 'way' in self.canvas.gettags(item):
                    self.parent.dict_way[item].frame.destroy()
                    del self.parent.dict_way[item]
                elif 'vehicle' in self.canvas.gettags(item):
                    self.parent.dict_vehicle[item].frame.destroy()
                    del self.parent.dict_vehicle[item]
                elif 'image' in self.canvas.gettags(item):
                    del self.parent.dict_image[item]
                self.canvas.delete(item)


class Create_Figure:

    def __init__(self, parent, x, y, figure):
        self.x0 = x
        self.y0 = y
        self.canvas = parent.canvas
        self.canvas.bind('<B1-Motion>', self.draw_figure)
        coord = [self.x0, self.y0, self.x0, self.y0]
        args = {'outline': parent.current_color,
                'fill': parent.current_bg_color,
                'width': parent.width_line.get(),
                'tags': figure}
        if figure == 'oval':
            self.figure = self.canvas.create_oval(coord, args)
        elif figure == 'rectangle':
            self.figure = self.canvas.create_rectangle(coord, args)
        elif figure == 'line':
            self.figure = self.canvas.create_line(coord, width=parent.width_line.get(),
                                                  fill=parent.current_color, tags=figure)
        elif figure == 'arrow':
            self.figure = self.canvas.create_line(coord, width=parent.width_line.get(),
                                                  fill=parent.current_color, tags=figure,
                                                  arrow='last', arrowshape='20 50 20')

        parent.list_move.append(range(self.figure, self.figure + 1))

    def draw_figure(self, event):
        self.canvas.coords(self.figure, self.x0, self.y0,
                           event.x, event.y)


class Grab:

    def __init__(self, parent, item, x, y):
        self.canvas = parent.canvas
        self.item = item
        if self.item[0] != parent.bg_id:
            self.canvas.bind('<B1-Motion>', self.relocate)
            self.old_x = x
            self.old_y = y
            self.canvas.tag_raise(self.item)

    def relocate(self, event):
        self.canvas.move(self.item, event.x - self.old_x, event.y - self.old_y)
        self.old_x = event.x
        self.old_y = event.y
