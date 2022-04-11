# dictionary for board information
board = {1: ' ' , 2: ' ' , 3: ' ' ,
       4: ' ' , 5: ' ' , 6: ' ' ,
       7: ' ' , 8: ' ' , 9: ' ' }

def instructions():
    print('Hello this is tic tac toe, the game\n')
    print('two players will take turns placing their pieces down\n')
    print('Player 1 is x and goes first\n')
    print('First to get a line wins\n')
    printInstructionBoard()

def printInstructionBoard():
    print('Here is the board\n')
    print('1|2|3')
    print('-+-+-')
    print('4|5|6')
    print('-+-+-')
    print('7|8|9')
    
# In order to keep track of players we will need a variable to hold that info
def game(player1,player2):
    player = 'X'
    count = 0
    try:
        while count <= 9:
            print("Player "+player+" it’s your turn")
            move = int(input())
            if(move >9 or move <1):
                print("Invalid number")
                continue
            if(board[move] == ' '):
                board[move] = player
                if(player=='X'):
                    player = 'O'
                else:
                    player = 'X'
            else:  
                print("Spot taken, pick another")
                continue
            count = count + 1

            # the minimum count (xoxox)
            if(count >= 5):
                # win scenarios (check all values around current move
                # horizontal
                # last value in row 3,6,9
    
                if(move%3 ==0):
                    if(board[move]==board[move-1]==board[move-2]!=' '):
                        winner(board[move])
                        break

                #middle    
                if( move%3==1):
                    if(board[move]==board[move+1]==board[move+2]!=' '):
                        winner(board[move])
                        break

                #first
                if(move%3 == 2):
                    if(board[move]==board[move+1]==board[move-1]!=' '):
                        winner(board[move])
                        break

                # vertical
                # last column 
                if(int((move-1)/3)==2):
                    if(board[move]==board[move-3]==board[move-6]!=' '):
                        winner(board[move])
                        break

                #middle column
                if(int((move-1)/3)==1):
                    if(board[move]==board[move+3]==board[move-3]!=' '):
                        winner(board[move])
                        break

                #first column
                if(int((move-1)/3)==0):
                    if(board[move]==board[move+3]==board[move+6]!=' '):
                        winner(board[move])
                        break

                # diagonals
                if(move == 1 or move == 5 or move == 9):
                    if(board[1]==board[5]==board[9]!=' '):
                        winner(board[move])
                        break

                if(move ==3 or move == 5 or move == 7):
                    if(board[3]==board[5]==board[7]!=' '):
                        winner(board[move])
                        break

            # tie scenario 
            if (count ==9):
                printBoard()
                print("TIE")
                break

            printBoard()

    except:
        print("An exception occurred")
 
# save results and print
def winner(player):
    print("The winner is "+player)

def printBoard():
    print(board[1]+"|"+board[2]+"|"+board[3])
    print("-----")
    print(board[4]+"|"+board[5]+"|"+board[6])
    print("-----")
    print(board[7]+"|"+board[8]+"|"+board[9])

# input player
def inputPlayers():
    print("Enter username of player 1: ")
    player1 = input()

    print("Enter username of player 2: ")
    player2 = input()

    return (player1,player2)

instructions()
a,b = inputPlayers()
game(a,b)