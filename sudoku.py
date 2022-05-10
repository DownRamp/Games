import random
import numpy as np

grid = []
fin_grid = []
happened = False


def make_sudoku(difficulty):
    global grid, fin_grid, happened
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    happened = False
    grid = [[0 for i in range(9)] for j in range(9)]

    random.shuffle(values)
    for i in range(9):
        grid[i][0] = values[i]

    generate()

    print("CREATED BASE GRID")
    squares_to_remove = 0
    if difficulty == 0:
        squares_to_remove = 36
    elif difficulty == 1:
        squares_to_remove = 46
    elif difficulty == 2:
        squares_to_remove = 52
    else:
        return

    print("STARTING CLEAN UP FOR SUDOKU PUZZLE")
    while squares_to_remove > 0:
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        if fin_grid[x][y] != 0:
            fin_grid[x][y] = 0
            squares_to_remove -= 1
    print(np.matrix(fin_grid))


def generate():
    global grid, happened, fin_grid
    if happened:
        return
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n):
                        grid[y][x] = n
                        generate()
                        grid[y][x] = 0
                return

    if not happened:
        fin_grid = list(map(list, grid))
        happened = True


def possible(y, x, n):
    global grid

    # check row
    count = 0
    for i in range(0, 9):
        if grid[y][i] == n:
            return False
    # check column
    for i in range(0, 9):
        if grid[i][x] == n:
            return False
    # check square
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[y0 + i][x0 + j] == n:
                return False
    return True


if __name__ == '__main__':
    difficulty = input("Enter difficulty 0-2: ")
    make_sudoku(int(difficulty))
