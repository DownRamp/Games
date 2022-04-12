import random
import copy
import array


def make_sudoku(difficulty):
    value = "123456789"

    while True:
        grid = []
        for i in range(9):
            grid.append(array.array('u', value))
            random.shuffle(grid[i])

        if check_solvable(grid):
            break
        print("CONINTUED")

    print("CREATED")
    squares_to_remove = 0
    if difficulty == 0:
        squares_to_remove = 36
    elif difficulty == 1:
        squares_to_remove = 46
    elif difficulty == 2:
        squares_to_remove = 52
    else:
        return

    print("STARTING SUDOKU")
    while squares_to_remove > 0:
        x = random.int(0, 9)
        y = random.int(0, 9)
        if grid[x][y] != 0:
            grid[x][y] = 0
            squares_to_remove -= 1
    print(grid)


def print_grid(grid):
    for i in range(9):
        for j in range(9):
            print("___")
            print(f"|{grid[i][j]}|")
            print("___")


def possible(y, x, n, grid):
    # check row
    count = 0
    for i in range(0, 9):
        if grid[y][i] == n:
            count +=1
    if count >1: return False
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


def check_solvable(grid):
    for y in range(9):
        for x in range(9):
            if not possible(y, x, grid[y][x], grid):
                return False
    return True


if __name__ == '__main__':
    difficulty = input("Enter difficulty 0-2: ")
    make_sudoku(int(difficulty))
