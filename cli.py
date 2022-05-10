import argparse
import sys
import tictactoe
import twenty_forty_8
 
list_games = ["2048", "snake", "sudoku", "checkers", "chess", "trucks", "tictactoe", "slot_machine"]
 
 
def read_user_cli_args():
  """ Handles the CLI user interactions.
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
      "-l",
      "--list",
      action="store_true",
      help="List of games",
  )
  return parser.parse_args()
 
 
def game_pick(game_select, instructions =False):
  try:
      if(game_select == list_games[6]):
          tictactoe.main()
      elif(game_select == list_games[0]):
          twenty_forty_8.main()
      else:
          print("BAD")
          sys.exit("Incorrect input -l to list games")
 
  except:
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
  print(user_args)
  if(user_args.list):
      game_list()
  elif(user_args.game):
      game_pick(user_args.game[1])
