import random
score = 0
gameOver = False
 
def instructions():
   print("The number 2 will appear in random spots and you will need to combine numbers to save space")
   print("If you run out of room the game ends")
   print("Commands are as follows : ")
   print("Up key or 'w' : Move Up")
   print("Down key or 's' : Move Down")
   print("Left key or 'a' : Move Left")
   print("Right key or 'd' : Move Right")
   print()
 
def main_game(n):
   global gameOver
   board = create_board(n)
 
   while not gameOver:
 
       add_2(board, n)
       print_board(board,n)
       cmd = input("Enter key: ")
       # move up, down, right, left
       if cmd == 'w': move_up(board,n)
       elif cmd == 's': move_down(board,n)
       elif cmd == 'a': move_left(board,n)
       elif cmd == 'd': move_right(board,n)
       else: print("Incorrect input")
 
       # print
       print_board(board,n)
 
def print_board(board,n): 
   global score
   for i in range(n):
       for j in range(n):
           val = board[i][j]
           if val > score:
               score = val
           print(f"|{val}|", end = '')
       print()
   print()
 
def move_up(board,n):
   for i in range(1,n):
       for j in range(n):
           if(board[i-1][j] == 0 and board[i][j] != 0):
               board[i-1][j] = board[i][j]
               board[i][j] = 0
               move_up(board,n)
           elif(board[i-1][j] == board[i][j]):
               board[i-1][j] = board[i][j]*2
               board[i][j] = 0
 

def move_down(board,n):
   for i in range(n-1):
       for j in range(n):
           if(board[i+1][j] == 0 and board[i][j] != 0):
               board[i+1][j] = board[i][j]
               board[i][j] = 0
               move_down(board,n)
           elif(board[i+1][j] == board[i][j]):
               board[i+1][j] = board[i][j]*2
               board[i][j] = 0
 
def move_left(board,n):
   for i in range(n):
       for j in range(1,n):
           if(board[i][j-1] == 0 and board[i][j] != 0):
               board[i][j-1] = board[i][j]
               board[i][j] = 0
               move_left(board,n)
           elif(board[i][j-1] == board[i][j]):
               board[i][j-1] = board[i][j]*2
               board[i][j] = 0
 
def move_right(board,n):
   for i in range(n):
       for j in range(n-1):
           if(board[i][j+1] == 0 and board[i][j] != 0):
               board[i][j+1] = board[i][j]
               board[i][j] = 0
               move_right(board,n)
          
           elif(board[i][j+1] == board[i][j]):
               board[i][j+1] = board[i][j]*2
               board[i][j] = 0
 
def create_board(n):
   board = []
   for i in range(n):
       board.append([0]*n)
   return board
 
# if all spots on board is taken
# if all values have no same values above or below
# regression
def game_over():
   global score, gameOver
   gameOver = True
   print(score)
 
# add a 2 to a random spot with a 0
def add_2(board, n):
   global gameOver
   inner_count = 0
 
   zero_x =[]
   zero_y =[]
 
   for i in range(n):
       for j in range(n):
           if(board[i][j] != 0):
               inner_count+=1
           else:
               zero_x.append(i)
               zero_y.append(j)
 
   if(inner_count == n*n):
       game_over()
 
   if(gameOver):
       return
 
   pos = random.randint(0,len(zero_x)-1)
   board[zero_x[pos]][zero_y[pos]] = 2


def main():
    instructions()
    main_game(4)


if __name__ == '__main__':
   instructions()
   main_game(4)