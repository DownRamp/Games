#!/usr/bin/env python
import tkinter as tk
from tkinter import *
import random
 
snakes = {5:1, 20:9, 24:17, 45:21, 33:11}
ladders = {8:13, 16:38, 19:22, 25:27, 35:45}
 
players = {}
 
class Player():
       def __init__(self):
               self.pos = 0
               self.name = ""
 
class NumberPlayers():
       def __init__(self,master):
               self.master = master
               self.frame = tk.Frame(master,padx=20, pady=50)
               self.lbl = Label(master , text = "Enter number of Players")
               self.lbl.pack()
               self.numPlay = Entry(master, width=30)
               self.numPlay.pack()
               self.btn = Button(master , text = "Start Game" , command = self.command )
               self.btn.pack()
               self.frame.pack(expand=True)
 
       def command(self):
               global players
               players = {}
               self.newWindow = tk.Toplevel(self.master)
               self.app = EnterNames(self.newWindow,int(self.numPlay.get()))
               # set players
               for i in range(int(self.numPlay.get())):
                       players[i] = Player()
 
class EnterNames():
       def __init__(self , master, num):
               self.choices = []
 
               self.num = num
               self.master = master
               master.title("Enter Names")
 
               self.frame = tk.Frame(master)
 
               for i in range(1,num+1):
                       player_label = "Player "+str(i)+" please enter name: "
                       label=Label(self.frame, text=player_label, font=('Aerial 12'))
                       label.pack()
                       ent = Entry(self.frame)
                       ent.pack()
                       self.choices.append(ent)
 
               self.enterButton = tk.Button(self.frame, text = 'Enter Usernames', width = 25 , command = self.command)
               self.enterButton.pack()
               self.frame.pack()
 
       def command(self):
               global players
               self.newWindow = tk.Toplevel(self.master)
               for i in range(self.num):
                       curr_player = players[i]
                       curr_player.name = self.choices[i].get()
               self.app = Main(self.newWindow,self.num)
 
class Main(): 
       def __init__(self , master, num):
               global players
               self.num = num
               self.master = master
               self.frame = tk.Frame(master)
               self.choices = []
               master.title("Snakes and Ladders")
 
               # Users turn to spin and display position on board
               text = tk.StringVar()
               player_label = "Player "+players[0].name+" your move"
               text.set(player_label)
               label=Label(self.frame, textvariable=text, font=('Aerial 18 underline'))
               label.pack()
               self.choices.append(text)
 
               for i in range(num):
                       text = tk.StringVar()
                       player_label = "Player "+players[i].name+" position "+str(players[i].pos)
                       text.set(player_label)
                       label=Label(self.frame, textvariable=text, font=('Aerial 12'))
                       label.pack()
                       self.choices.append(text)
 
               text = tk.StringVar()
               player_label = "Last Move"
               text.set(player_label)
               label=Label(self.frame, textvariable=text, font=('Aerial 18 underline'))
               label.pack()
               self.choices.append(text)
 
               self.selection = 0
               self.spinButton = tk.Button(self.frame, text = 'Spin', width = 25, command = self.move)
               self.spinButton.pack()
 
               self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25 , command = self.close_window)
               self.quitButton.pack()
               self.frame.pack()
 
       def move(self):
               global players
               command = self.spin()
               self.choices[self.selection+1].set("Player "+players[self.selection].name+" position "+str(players[self.selection].pos))
               self.selection +=1
               if(self.selection >=self.num):
                       self.selection = 0
               self.choices[0].set("Player "+players[self.selection].name+" your move")
               self.choices[len(self.choices)-1].set(command)
 
       def spin(self):
               global players
               curr_pos = players[self.selection].pos
               spin_value = random.randint(2, 12)
               curr_pos += spin_value
               command = players[self.selection].name+" "
               if(curr_pos == 50):
                       print("WINNER "+players[self.selection].name)
                       self.close_window()
               elif(curr_pos in snakes):
                       curr_pos = snakes[curr_pos]
                       command+=" SNAKES! "
               elif(curr_pos in ladders):
                       curr_pos = ladders[curr_pos]
                       command+=" LADDERS! "
               elif(curr_pos > 50):
                       curr_pos = 50 - (curr_pos%50)
               players[self.selection].pos = curr_pos
               command+=str(curr_pos)
               return command
               
       def close_window(self):
               self.master.destroy()
               sys.exit()
 
if __name__ == '__main__':
       # initial clearing of dictionary
       root = Tk()
 
       root.title("window")
 
       root.geometry("350x100")
 
       cls = NumberPlayers(root)
 
       root.mainloop()
