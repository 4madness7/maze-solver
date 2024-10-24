from graphics import Cell
from time import sleep
import random


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None) -> None:
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        if seed:
            random.seed(seed)
        self._create_cells()

    def _create_cells(self):
        for _ in range(self.num_rows):
            row = []
            for _ in range(self.num_cols):
                row.append(Cell(self.win))
            self._cells.append(row)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cell(i, j)

        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _draw_cell(self, i, j):
        x1 = (j + 1) * self.x1
        y1 = (i + 1) * self.y1
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self.win:
            self.win.redraw()
            sleep(0.03)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_left_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_rows-1][self.num_cols-1].has_right_wall = False
        self._draw_cell(self.num_rows-1, self.num_cols-1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            possible_directions = []
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                possible_directions.append((i - 1, j))
            # right
            if i < self.num_rows - 1 and not self._cells[i + 1][j].visited:
                possible_directions.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                possible_directions.append((i, j - 1))
            # down
            if j < self.num_cols - 1 and not self._cells[i][j + 1].visited:
                possible_directions.append((i, j + 1))

            if len(possible_directions) == 0:
                self._draw_cell(i, j)
                return

            new_i, new_j = random.choice(possible_directions)

            # new cell on top
            if new_i == i - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[new_i][new_j].has_bottom_wall = False

            # new cell on bottom
            if new_i == i + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[new_i][new_j].has_top_wall = False

            # new cell on left
            if new_j == j - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[new_i][new_j].has_right_wall = False

            # new cell on right
            if new_j == j + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[new_i][new_j].has_left_wall = False

            self._break_walls_r(new_i, new_j)

    def _reset_cells_visited(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True

        if (not self._cells[i][j].has_right_wall and
            j != self.num_cols - 1 and
            not self._cells[i][j + 1].visited):
                self._cells[i][j].draw_move(self._cells[i][j + 1])
                finished = self._solve_r(i, j + 1)
                if finished:
                    return True
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        if (not self._cells[i][j].has_bottom_wall and
            i != self.num_rows - 1 and
            not self._cells[i + 1][j].visited):
                self._cells[i][j].draw_move(self._cells[i + 1][j])
                finished = self._solve_r(i + 1, j)
                if finished:
                    return True
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        if (not self._cells[i][j].has_left_wall and
            j > 0 and
            not self._cells[i][j - 1].visited):
                self._cells[i][j].draw_move(self._cells[i][j - 1])
                finished = self._solve_r(i, j - 1)
                if finished:
                    return True
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        if (not self._cells[i][j].has_top_wall and
            i > 0  and
            not self._cells[i - 1][j].visited):
                self._cells[i][j].draw_move(self._cells[i - 1][j])
                finished = self._solve_r(i - 1, j)
                if finished:
                    return True
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        return False



