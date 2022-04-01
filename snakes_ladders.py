import tkinter as tk
import tkinter as tk
from tkinter import ttk

import random
snakes = {5:1, 20:9, 24:17, 45:21, 33:11}
ladders = {8:13, 16:38, 19:22, 25:27, 35:45}

def Game_Window():
    Window = tk.Toplevel()
    canvas = tk.Canvas(Window, height=HEIGHT, width=WIDTH)
    canvas.pack()
    
HEIGHT = 300
WIDTH = 500

ws = tk.Tk()
ws.title("Snakes and ladders")
ws.config(bg="#447c84")
ws.attributes('-fullscreen',True)
canvas = tk.Canvas(ws, height=HEIGHT, width=WIDTH)
canvas.pack()

ws.Label(
    canvas, 
    text="Enter number of players",
    font=("Times", "24", "bold")
    ).grid(row=0, columnspan=3, pady=10)
numPlayers = ws.Entry(canvas, width=30)

button = tk.Button(ws, text="Start Game", bg='White', fg='Black',
                              command=lambda: Game_Window())

button.pack()
ws.mainloop()

def rollDice():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return dice1 + dice2

def game():
    #show gui
    # put in number of players
    players = {}
    players[inputName] = 0
    while True:
        for player in players:
            print("")
    # show position on board
    # roll dice, random number generator

    # if position in snakes or ladder update positions
    # if 50 position 
    # if not perfect roll go back
    print("asdf")