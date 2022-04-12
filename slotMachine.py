import time
import threading
 
f = True
s = True
t = True
 
count = 0
 
def get_input():
   global count,f,s,t
   data = input()
   if(count == 0):
       count+=1
       f = False
  
   elif(count == 1):
       count+=1
       s = False
  
   elif(count == 2):
       count+=1
       t = False
  
   return data
 
def game():
   global f,s,t, count
 
   wallet = 100
   spin_cost = 8
 
   while(wallet >0):
       wallet = wallet - spin_cost
       first = 0
       second = 0
       third = 0
       count = 0
       f1 = True
       s1 = True
       t1 = True
       f = True
       s = True
       t = True
 
       while True:
           if(f):
               first = rand_gen(0,5)
               if(f1):
                   input_thread = threading.Thread(target=get_input)
                   input_thread.start()
                   f1 = False
           elif(s):
               second = rand_gen(0,5)
               if(s1 and not f):
                   input_thread = threading.Thread(target=get_input)
                   input_thread.start()
                   s1 = False
           elif(t):
               third = rand_gen(0,5)
               if(t1 and not f and not s):
                   input_thread = threading.Thread(target=get_input)
                   input_thread.start()
                   t1 = False
           else:
               break
           roll = '{:1d}:{:1d}:{:1d}'.format(first,second,third)
           print(roll, end ="\r")
           time.sleep(1)
 
       # gain check
       gain = first + second + third
       wallet = wallet + gain
       win = str(gain)
       print("winner: "+win)
   print("Gameover")
 
def rand_gen(start, end):
   # get seed
   f = open("assets/seed.txt", "r")
   seed = int(f.read())
   mut = seed * seed
   new_string = str(mut)[0:9]
   new_seed = new_string[1:len(new_string)-1]
 
   # change seed for next use
   c = open("assets/seed.txt", "w")
   c.write(new_seed)
 
   for i in new_seed:
       num = int(i)
       if(start <= num and end >= num):
           return num
 
   return rand_gen(start,end)
 
game()
