from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height) -> None:
        self.root = Tk()
        self.root.title("Maze solver")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.canvas = Canvas(self.root, bg="white", height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)

        self.running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)

    def redraw(self) -> None:
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self) -> None:
        self.running = True
        while self.running:
            self.redraw()
        print("Window closed...")

    def close(self) -> None:
        self.running = False

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color) -> None:
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
       )

class Cell:
    def __init__(self, window=None) -> None:
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._win = window
        self.visited = False

    def draw(self, x1, y1, x2, y2) -> None:
        if self._win is None:
            return
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        fill = "black"
        if not self.has_top_wall:
            fill = "white"
        l = Line(Point(x1, y1), Point(x2, y1))
        self._win.draw_line(l, fill)

        fill = "black"
        if not self.has_right_wall:
            fill = "white"
        l = Line(Point(x2, y1), Point(x2, y2))
        self._win.draw_line(l, fill)

        fill = "black"
        if not self.has_bottom_wall:
            fill = "white"
        l = Line(Point(x2, y2), Point(x1, y2))
        self._win.draw_line(l, fill)

        fill = "black"
        if not self.has_left_wall:
            fill = "white"
        l = Line(Point(x1, y2), Point(x1, y1))
        self._win.draw_line(l, fill)

    def draw_move(self, to_cell, undo=False) -> None:
        fill_color = "red"
        if undo:
            fill_color = "gray"
        if self._x1 and self._x2 and self._y1 and self._y2 and self._win:
            center_self = Point((self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2)
            center_to_cell = Point((to_cell._x1 + to_cell._x2) // 2, (to_cell._y1 + to_cell._y2) // 2)
            self._win.draw_line(Line(center_self, center_to_cell), fill_color)

