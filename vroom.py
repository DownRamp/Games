import pygame
from tkinter import *
from tkinter import messagebox
import sys 
import pygame_menu

window_x = 1000
window_y = 1000
black = (0,0,0)
 
x =  (window_x/2)
y = (window_y/2)
x_change = 0
y_change = 0
car_speed = 0
 
race_end = False
rectangle_draging = False
opened = False

car_image = 'images/racecar.png'
racecar = pygame.image.load(car_image)
car_num = 0
car_selection = ['images/racecar.png','images/racecar3.png','images/rsz_racecar2.jpg']
 
gameDisplay = pygame.display.set_mode((window_x,window_y))

root = Tk()

def close():
    root.destroy()

def pick(selected, value):
    global car_image, car_selection, car_num, racecar
    car_num = value
    car_image = car_selection[car_num]
    racecar = pygame.image.load(car_image)
    
def car(x,y):
    gameDisplay.blit(racecar, (x,y))

def start_the_game():
    global race_end, rectangle_draging,x, y,x_change,y_change ,car_speed, racecar, car_image
    pygame.display.set_caption('Race')
    racecar = pygame.image.load(car_image)
    racecar.convert()
    rect = racecar.get_rect()
    rect.center = window_x//2, window_y//2
    while not race_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                race_end = True
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5
                elif event.key == pygame.K_TAB:
                    if(not opened):
                        opened = True
                        pick()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:            
                    if rect.collidepoint(event.pos):
                        rectangle_draging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = x - mouse_x
                        offset_y = y - mouse_y

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:            
                    rectangle_draging = False

            if event.type == pygame.MOUSEMOTION:
                if rectangle_draging:
                    mouse_x, mouse_y = event.pos
                    x = mouse_x + offset_x
                    y = mouse_y + offset_y

        x += x_change
        y += y_change

        if(x >=1000 or y >= 1000):
            # crash
            Tk().wm_withdraw()
            messagebox.showinfo('You crashed BYE BYE')
            pygame.quit()
            sys.exit()

        gameDisplay.fill(black)
        car(x,y)
        
        pygame.display.update()
pygame.init()

menu = pygame_menu.Menu('Welcome to racing', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name:', default='John Doe')
menu.add.selector('Car:', [('1', 0), ('2', 1), ('3',2)], onchange=pick)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(gameDisplay)

pygame.quit()
quit()