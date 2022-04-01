import argparse
import sys
 
list_games = ["2042","snake", "sudoku", "tetris", "checkers", "chess", "trucks", "tictactoe", "slot_machine"]
 
def read_user_cli_args():
   """Handles the CLI user interactions.
 
   Returns:
       argparse.Namespace: Populated namespace object
   """
   parser = argparse.ArgumentParser(
       description="Starts a game"
   )
   parser.add_argument(
       "game", nargs="+", type=str, help="enter the game name"
   )
   parser.add_argument(
       "-i",
       "--instructions",
       action="store_true",
       help="Instructions for game",
   )
   parser.add_argument(
       "-l",
       "--list",
       action="store_true",
       help="List of games",
   )
   return parser.parse_args()
 
def game_pick(game_select, instructions =False):
   try:
       if(game_select[0] == "tictactoe"):
           print("tic tac toe")
       elif(game_select[0] == "2042"):
           print("2042")
   except error:
       sys.exit("ERROR")
 
def game_list():
   global list_games
   print("-------------")
   print("    GAMES    ")
   print("-------------")
 
   for game in list_games:
      print(game+"\n")
 
if __name__ == "__main__":
   user_args = read_user_cli_args()
   if(not user_args.list):
       game_pick(user_args.game[0], user_args.instructions)
   else:
       game_list()
