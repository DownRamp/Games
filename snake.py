import pygame
import time
import random
pygame.init()
background_color = (255, 255, 255)
food_color = (213, 50, 80)
snake_color = (0, 255, 0)
width = 1000
height = 700
block = 20
half_block = block/2
snake_speed = 25
 
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake!!!!!!')
clock = pygame.time.Clock()
def snake(snake_body):
  for x in snake_body:
      pygame.draw.rect(display, snake_color, [x[0], x[1], block, block])
 
def gen_food():
   food = random.randint(block,width-block), random.randint(block,height-block)
   return food
 
def game():
   game_over = False
   x = 500
   y = 500
   snake_body = []
   snake_size = 1
   food = gen_food()
 
   x_change = 0
   y_change = 0
 
   while not game_over:
 
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               game_over = True
 
           if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  x_change = -half_block
                  y_change = 0
              elif event.key == pygame.K_RIGHT:
                  x_change = half_block
                  y_change = 0
              elif event.key == pygame.K_UP:
                  y_change = -half_block
                  x_change = 0
              elif event.key == pygame.K_DOWN:
                  y_change = half_block
                  x_change = 0
 
       x += x_change
       y += y_change
 
       if y >= height or y<0 or x >=width or x<0:
           game_over = True
 
       display.fill(background_color)
 
       snake_head = []
       snake_head.append(x)
       snake_head.append(y)
 
       for snake_bit in snake_body[:-1]:
           if(snake_bit == snake_head):
               game_over = True
              
       snake_body.append(snake_head)
       if(len(snake_body) > snake_size):
           del snake_body[0]
 
       snake(snake_body)
 
       max_x = x+block
       min_x = x-block
       max_y = y+block
       min_y = y-block
 
       if max_x >= width:
           max_x = width
       if min_x < 0:
           min_x = 0
       if max_y >= height:
           max_y = height
       if min_y < 0:
           min_y = 0
 
       if(food[0] >= min_x and food[0] <= max_x and food[1] >= min_y and food[1] <= max_y):
           snake_size+=1
           food= gen_food()
 
       pygame.draw.rect(display, food_color, [food[0], food[1], block, block])
 
       pygame.display.update()
       clock.tick(snake_speed)
 
   print("Score: " +str(snake_size))
   pygame.quit()
   quit()
game()
