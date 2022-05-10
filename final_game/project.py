import pygame
import os
import sys
import random
import math
import time

bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

move_size = 20
jump_size = 50
red = (255, 0, 0)
green = (0, 255, 0)

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


class Player(_Physics, pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, speed, name, health, lives, jumps):
        _Physics.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = []
        self.name = name
        self.strength = 10
        self.pos_y = pos_y
        self.pos_x = pos_x
        if(self.name == "Knight"):
            self.dir = "right"
        else:
            self.dir = "left"

        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.max_hp = health
        self.hp = health
        self.flip = False
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
        self.rect.center = (pos_x, pos_y)
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
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
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

    def draw(self, surface):
        surface.blit(self.image, self.rect)

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
            #         damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
            #         damage_text_group.add(damage_text)
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
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()


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
    def __init__(self, screen, x, y, hp, max_hp):
        self.screen = screen
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        #update with new health
        self.hp = hp
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(self.screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(self.screen, green, (self.x, self.y, 150 * ratio, 20))

class Control(object):

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.keys = pygame.key.get_pressed()
        self.done = False
        self.player1 = Player(screen_width/2, (screen_height-bottom_panel)/2, 4, 'Knight', 100, 3, 1)
        self.player2 = Player((screen_width-50)/2, (screen_height-bottom_panel)/2, 4, 'Bandit', 100, 3, 1)
        self.game_over = False
        self.win = False
        moving_sprites = pygame.sprite.Group()
        moving_sprites.add(self.player1)
        moving_sprites.add(self.player2)

        self.level = pygame.Surface((screen_width, screen_height-bottom_panel-10)).convert()
        self.level_rect = self.level.get_rect()
        self.viewport = self.screen.get_rect(bottom=self.level_rect.bottom)
        self.win_text, self.win_rect = self.make_text()
        self.obstacles = self.make_obstacles()
        self.background_img = pygame.image.load('img/Background/background.png').convert_alpha()
        self.panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
        # button images
        self.potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()
        self.restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()
        # load victory and defeat images
        self.victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
        self.defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()
        # sword image
        self.sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()
        self.font = pygame.font.SysFont('Times New Roman', 26)
        self.player1_health_bar = HealthBar(self.screen, 100, screen_height - bottom_panel + 40, self.player1.hp, self.player1.max_hp)
        self.player2_health_bar = HealthBar(self.screen, 550, screen_height - bottom_panel + 40, self.player2.hp, self.player2.max_hp)

    def make_text(self):
        font = pygame.font.Font(None, 100)
        message = "You win. Celebrate."
        text = font.render(message, True, (100, 100, 175))
        rect = text.get_rect(centerx=self.level_rect.centerx, y=100)
        return text, rect

    def make_obstacles(self):
        floor = Block(pygame.Color("black"), (100, screen_height - bottom_panel, 890, 10))
        static = []
        # (250, 780, 200, 100)
        top = 500
        for i in range(4):
            left = random.randint(100, 980)
            top += 100
            static.append(Block(pygame.Color("black"), (left, top, 200, 25)))
        return pygame.sprite.Group(floor, static)

    def update_viewport(self, speed):
        for i in (0, 1):
            first_third = self.viewport[i] + self.viewport.size[i] // 3
            second_third = first_third + self.viewport.size[i] // 3
            player_center = self.player1.rect.center[i]
            mult = 0
            if speed[i] > 0 and player_center >= first_third:
                mult = 0.5 if player_center < self.viewport.center[i] else 1
            elif speed[i] < 0 and player_center <= second_third:
                mult = 0.5 if player_center > self.viewport.center[i] else 1
            self.viewport[i] += mult * speed[i]
        self.viewport.clamp_ip(self.level_rect)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    self.player1.jump(self.obstacles)
                elif event.key == pygame.K_RSHIFT:
                    self.player2.jump(self.obstacles)
                elif event.key == pygame.K_f:
                    self.player1.attack(self.player2)
                elif event.key == pygame.K_j:
                    self.player2.attack(self.player1)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player1.jump_cut()
                elif event.key == pygame.K_f:
                    self.player1.jump_cut()

    def update(self):
        self.keys = pygame.key.get_pressed()
        self.player1.pre_update(self.obstacles)
        self.player2.pre_update(self.obstacles)

        self.obstacles.update(self.player1, self.obstacles)
        self.player1.update(self.obstacles, self.keys)
        self.obstacles.update(self.player2, self.obstacles)
        self.player2.update(self.obstacles, self.keys)

        self.update_viewport(self.player1.total_displacement)
        self.update_viewport(self.player2.total_displacement)

    def draw(self):
        self.draw_bg()
        self.obstacles.draw(self.level)
        if self.win:
            self.level.blit(self.win_text, self.win_rect)
        self.draw_panel(self.player1, self.player2, self.font, (255, 0, 0))
        self.player1.update(self.obstacles, self.keys)
        self.player2.update(self.obstacles, self.keys)
        self.player1.draw(self.level)
        self.player2.draw(self.level)
        self.player1_health_bar.draw(self.player1.hp)
        self.player2_health_bar.draw(self.player2.hp)
        self.screen.blit(self.level, (0, 0), self.viewport)

    def display_fps(self):
        caption = "{} - FPS: {:.2f}".format("FIGHT KNIGHT", self.clock.get_fps())
        pygame.display.set_caption(caption)

    def main_loop(self):
        while not self.done:
            # draw background
            # draw panel
            # self.draw_panel()
            self.event_loop()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.fps)
            self.display_fps()

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    #function for drawing background
    def draw_bg(self):
        self.level.blit(self.background_img, (0, 0))

    def draw_panel(self, player1, player2, font, color):
        #draw panel rectangle
        self.screen.blit(self.panel_img, (0, screen_height - bottom_panel))
        txt = f"{player1.name} HP: {player1.hp}"
        y = (screen_height - bottom_panel + 10)
        #show knight stats
        self.draw_text(txt, font, color, 100, y)

if __name__ == "__main__":
    pygame.init()
    # menu -> character select -> game
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Battle')

    clock = pygame.time.Clock()

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    run_it = Control()
    run_it.main_loop()
    pygame.quit()
    sys.exit()
