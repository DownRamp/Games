import pygame
import random
import os
import sys
import math
import time

class _Physics(object):
    def __init__(self):
        self.velocity = [0, 0]
        self.grav = 0.4
        self.fall = False

    def physics_update(self):
        if self.fall:
            self.velocity[1] += self.grav
        else:
            self.velocity[1] = 0

class Fighter(_Physics, pygame.sprite.Sprite):
	def __init__(self, x, y, name, max_hp, lives, jumps, speed):
	    _Physics.__init__(self)
	    pygame.sprite.Sprite.__init__(self)
        self.strength = 10
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.alive = True
		self.animation_list = []
		self.frame_index = 0
		self.action = 0#0:idle, 1:attack, 2:hurt, 3:dead
		self.update_time = pygame.time.get_ticks()
		self.flip = False
        self.frame_start_pos = None
        self.total_displacement = None
        self.speed = speed
        self.jump_power = -9.0
        self.jump_cut_magnitude = -3.0
        self.on_moving = False
        self.collide_below = False
        self.attack_animation = False
        self.lives = lives
        self.jumps = jumps

		if(self.name == "Knight"):
            self.dir = "right"
        else:
            self.dir = "left"
		#load idle images
		temp_list = []
		for i in range(8):
			img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load attack images
		temp_list = []
		for i in range(8):
			img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load hurt images
		temp_list = []
		for i in range(3):
			img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load death images
		temp_list = []
		for i in range(10):
			img = pygame.image.load(f'img/{self.name}/Death/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.x = x
		self.y = y

    def check_keys(self, keys):
        self.velocity[0] = 0
        if self.name == "Knight":
            if keys[pygame.K_a]:
                if self.dir == "right":
                    self.dir = "left"
                    self.flip = not self.flip
                self.velocity[0] -= self.speed
            if keys[pygame.K_d]:
                if self.dir == "left":
                    self.dir = "right"
                    self.flip = not self.flip
                self.velocity[0] += self.speed
        else:
            if keys[pygame.K_LEFT]:
                if self.dir == "right":
                    self.dir = "left"
                    self.flip = not self.flip
                self.velocity[0] -= self.speed
            if keys[pygame.K_RIGHT]:
                if self.dir == "left":
                    self.dir = "right"
                    self.flip = not self.flip
                self.velocity[0] += self.speed

    def get_position(self, obstacles):
        if not self.fall:
            self.check_falling(obstacles)
        else:
            self.fall = self.check_collisions((0,self.velocity[1]),1,obstacles)
        if self.velocity[0]:
            self.check_collisions((self.velocity[0],0), 0, obstacles)

    def check_falling(self, obstacles):
        if not self.collide_below:
            self.fall = True
            self.on_moving = False

    def check_moving(self, obstacles):
        if not self.fall:
            now_moving = self.on_moving
            any_moving, any_non_moving = [], []
            for collide in self.collide_below:
                if collide.type == "moving":
                    self.on_moving = collide
                    any_moving.append(collide)
                else:
                    any_non_moving.append(collide)
            if not any_moving:
                self.on_moving = False
            elif any_non_moving or now_moving in any_moving:
                self.on_moving = now_moving

    def check_collisions(self, offset, index, obstacles):
        unaltered = True
        self.rect[index] += offset[index]
        while pygame.sprite.spritecollideany(self, obstacles):
            self.rect[index] += (1 if offset[index]<0 else -1)
            unaltered = False
        return unaltered

    def check_above(self, obstacles):
        self.rect.move_ip(0, -1)
        collide = pygame.sprite.spritecollideany(self, obstacles)
        self.rect.move_ip(0, 1)
        return collide

    def check_below(self, obstacles):
        self.rect.move_ip((0,1))
        collide = pygame.sprite.spritecollide(self, obstacles, False)
        self.rect.move_ip((0,-1))
        return collide

    def jump(self, obstacles):
        if not self.fall and not self.check_above(obstacles):
            self.velocity[1] = self.jump_power
            self.fall = True
            self.on_moving = False

    def jump_cut(self):
        if self.fall:
            if self.velocity[1] < self.jump_cut_magnitude:
                self.velocity[1] = self.jump_cut_magnitude

    def pre_update(self, obstacles):
        self.frame_start_pos = self.rect.topleft
        self.collide_below = self.check_below(obstacles)
        self.check_moving(obstacles)

	def update(self, obstacles, keys):
		animation_cooldown = 100
		self.check_keys(keys)
        self.get_position(obstacles)
        self.physics_update()
        start = self.frame_start_pos
        end = self.rect.topleft
        self.total_displacement = (end[0]-start[0], end[1]-start[1])
        if self.flip:
            self.image = pygame.transform.flip(self.animation_list[self.action][self.frame_index], True, False)
        else:
            self.image = self.animation_list[self.action][self.frame_index]
		#handle animation
		#update image
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
        if self.rect.center[0] <0 or self.rect.center[1] <0 or self.rect.center[0] > screen_width or self.rect.center[1] > screen_height:
            self.death()
        #if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
                if self.lives <0:
                    print("gameover")
                else:
                    self.reset()
            else:
                self.idle()

	def idle(self):
		#set variables to idle animation
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()


	def attack(self, target):
	    dist = math.dist([target.rect.center[0], target.rect.center[1]],[self.rect.center[0], self.rect.center[1]])
        if dist < 100:
            #deal damage to enemy
            rand = random.randint(-5, 5)
            damage = self.strength + rand
            target.hp -= damage
            #run enemy hurt animation
            target.hurt()
            #check if target has died
            if target.hp < 1:
                target.hp = 0
                target.alive = False
                target.death()
            #set variables to attack animation
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        else:
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

	def hurt(self):
		#set variables to hurt animation
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def death(self):
		#set variables to death animation
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()
        self.lives -=1

	def reset (self):
		self.alive = True
		self.
		self.hp = self.max_hp
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()
        self.rect.center = (self.x, self.y)

	def draw(self):
		screen.blit(self.image, self.rect)


class Block(pygame.sprite.Sprite):
    """A class representing solid obstacles."""
    def __init__(self, color, rect):
        """The color is an (r,g,b) tuple; rect is a rect-style argument."""
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface(self.rect.size).convert()
        self.image.fill(color)
        self.type = "normal"

class HealthBar():
	def __init__(self, x, y, hp, max_hp):
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp

	def draw(self, hp):
		#update with new health
		self.hp = hp
		#calculate health ratio
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))



class DamageText(pygame.sprite.Sprite):
	def __init__(self, x, y, damage, colour):
		pygame.sprite.Sprite.__init__(self)
		self.image = font.render(damage, True, colour)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0


	def update(self):
		#move damage text up
		self.rect.y -= 1
		#delete the text after a few seconds
		self.counter += 1
		if self.counter > 30:
			self.kill()

class Control(object):
#     def __init__(self):

    pygame.init()

    clock = pygame.time.Clock()
    fps = 60

    #game window
    bottom_panel = 150
    screen_width = 800
    screen_height = 400 + bottom_panel
    move_size = 20
    jump_size = 50
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Fight Knight')

    #define fonts
    font = pygame.font.SysFont('Times New Roman', 26)

    #define colours
    red = (255, 0, 0)
    green = (0, 255, 0)

    #load images
    #background image
    background_img = pygame.image.load('img/Background/background.png').convert_alpha()
    #panel image
    panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
    #load victory and defeat images
    victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
    defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()


    #create function for drawing text
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))


    #function for drawing background
    def draw_bg():
        screen.blit(background_img, (0, 0))

    def make_obstacles(self):
        floor = Block(pygame.Color("darkgreen"), (100, screen_height - bottom_panel, 890, 10))
        static = []
        # (250, 780, 200, 100)
        top = 0
        for i in range(4):
            left = random.randint(100, 980)
            top += 100
            static.append(Block(pygame.Color("darkgreen"), (left, top, 200, 25)))
        return pygame.sprite.Group(floor, static)

    def draw_panel(player1, player2):
        #draw panel rectangle
        screen.blit(panel_img, (0, screen_height - bottom_panel))
        #show knight stats
        draw_text(f'{player1.name} HP: {player1.hp}', font, red, 100, screen_height - bottom_panel + 10)
        draw_text(f'{player2.name} HP: {player2.hp}', font, red, 100, screen_height - bottom_panel + 70)

    damage_text_group = pygame.sprite.Group()
    x, y, name, max_hp, lives, jumps, speed)
    player1 = Fighter(200, 260, 'Knight', 100, 3, 1, 4)
    player2 = Fighter(550, 270, 'Bandit', 100, 3, 1,4 )
    player1_health_bar = HealthBar(100, screen_height - bottom_panel + 40, player1.hp, player1.max_hp)
    player2_health_bar = HealthBar(100, screen_height - bottom_panel + 40, player2.hp, player2.max_hp)

    run = True
    while run:

        clock.tick(fps)

        #draw background
        draw_bg()

        #draw panel
        draw_panel()
        knight_health_bar.draw(knight.hp)
        bandit_health_bar.draw(bandit.hp)

        #draw fighters
        knight.update()
        knight.draw()
        for bandit in bandit_list:
            bandit.update()
            bandit.draw()

        #draw the damage text
        damage_text_group.update()
        damage_text_group.draw(screen)

        #control player actions
        #reset action variables
        attack = False
        potion = False
        target = None
        #make sure mouse is visible
        pygame.mouse.set_visible(True)
        for count, bandit in enumerate(bandit_list):
            if bandit.rect.collidepoint(pos):
                #hide mouse
                pygame.mouse.set_visible(False)
                #show sword in place of mouse cursor
                screen.blit(sword_img, pos)
                if clicked == True and bandit.alive == True:
                    attack = True
                    target = bandit_list[count]

        if game_over == 0:
            #player action
            if knight.alive == True:
                if current_fighter == 1:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        #look for player action
                        #attack
                        if attack == True and target != None:
                            knight.attack(target)
                        #potion
                        if potion == True:
                            if knight.potions > 0:
                                #check if the potion would heal the player beyond max health
                                if knight.max_hp - knight.hp > potion_effect:
                                    heal_amount = potion_effect
                                else:
                                    heal_amount = knight.max_hp - knight.hp
                                knight.hp += heal_amount
                                knight.potions -= 1
                                damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                                damage_text_group.add(damage_text)
                                current_fighter += 1
                                action_cooldown = 0
            else:
                game_over = -1


            #enemy action
            for count, bandit in enumerate(bandit_list):
                if current_fighter == 2 + count:
                    if bandit.alive == True:
                        action_cooldown += 1
                        if action_cooldown >= action_wait_time:
                            #check if bandit needs to heal first
                            if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
                                #check if the potion would heal the bandit beyond max health
                                if bandit.max_hp - bandit.hp > potion_effect:
                                    heal_amount = potion_effect
                                else:
                                    heal_amount = bandit.max_hp - bandit.hp
                                bandit.hp += heal_amount
                                bandit.potions -= 1
                                damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)
                                damage_text_group.add(damage_text)
                                current_fighter += 1
                                action_cooldown = 0
                            #attack
                            else:
                                bandit.attack(knight)
                                current_fighter += 1
                                action_cooldown = 0
                    else:
                        current_fighter += 1

            #if all fighters have had a turn then reset
            if current_fighter > total_fighters:
                current_fighter = 1


        #check if all bandits are dead
        alive_bandits = 0
        for bandit in bandit_list:
            if bandit.alive == True:
                alive_bandits += 1
        if alive_bandits == 0:
            game_over = 1


        #check if game is over
        if game_over != 0:
            if game_over == 1:
                screen.blit(victory_img, (250, 50))
            if game_over == -1:
                screen.blit(defeat_img, (290, 50))
    # 		if restart_button.draw():
    # 			knight.reset()
    # 			for bandit in bandit_list:
    # 				bandit.reset()
    # 			game_over = 0



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    Control()
