from graphics import Line, Point, Window, Cell
from maze import Maze
from time import sleep

if __name__ == "__main__":
    width = 800
    height = 600
    win = Window(width, height)

    cell_size_x = 50
    cell_size_y = 50
    num_rows = (height - 100) // cell_size_x
    num_cols = (width - 100) // cell_size_y
    maze = Maze(50, 50, num_rows, num_cols, cell_size_x, cell_size_y, win)

    maze.solve()

    win.wait_for_close()
