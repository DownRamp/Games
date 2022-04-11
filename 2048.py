import random

score = 0

def instructions():
    print("The number 2 will appear in random spots and you will need to combine numbers to save space")
    print("If you run out of room the game ends")
    print("Commands are as follows : ")
    print("'w' : Move Up")
    print("'s' : Move Down")
    print("'a' : Move Left")
    print("'d' : Move Right")

def main_game(n):
    board = create_board(n)
    game_over = False
    while not game_over:
        add_2(board, n)
        # move up, down, right, left
        move = input("Enter command")
        make_move(move)
        # print 
        print_board(n)

def make_move(move):
    if(move=='w'):
        # squish up
    elif(move=='s'):
        # squish down
    elif(move=='a'):
        #squish left
    elif(move=='d'):
        #squish right
    else:
        print("INCORRECT MOVE INPUT")
        new_move = input("Enter command")
        make_move(new_move)
        
def create_board(n):
    board = []
    for i in range(n):
        board.append([0]*n)
    return board

# return list of x,y coords for all zero locations
def check_zeros(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            print(board[i][j])
def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            print(board[i][j])
# if all spots on board is taken
# if all values have no same values above or below
# regression
def game_over_check():
    global score
    print(score)
# add a 2 to a random spot with a 0
def add_2(board, n):
    inner_count = 0
    for
    if(inner_count!= 0):
        game_over_check()
    if(gameOver):
        return
    x = random.randint(0,n-1)
    y = random.randint(0,n-1)

if __name__ == '__main__':
    instructions()
    main_game(5)
