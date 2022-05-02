import pygame
import os
import sys
import random

bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

move_size = 20
jump_size = 50


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
        # change later
        self.image = pygame.Surface((30,55)).convert()
        self.image.fill(pygame.Color("red"))
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.frame_start_pos = None
        self.total_displacement = None
        self.speed = speed
        self.jump_power = -9.0
        self.jump_cut_magnitude = -3.0
        self.on_moving = False
        self.collide_below = False

        self.attack_animation = False
        # self.sprites = []
        # self.current_sprite = 0
        # self.image = self.sprites[self.current_sprite]

        self.name = name
        self.health = health
        self.lives = lives
        self.jumps = jumps

        # self.rect = self.image.get_rect()
        # self.rect.topleft = [pos_x, pos_y]

    def check_keys(self, keys):
        self.velocity[0] = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity[0] -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity[0] += self.speed

    def attack(self):
        self.attack_animation = True

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
        self.check_keys(keys)
        self.get_position(obstacles)
        self.physics_update()
        start = self.frame_start_pos
        end = self.rect.topleft
        self.total_displacement = (end[0]-start[0], end[1]-start[1])
        # if self.attack_animation == True:
        #     self.current_sprite += speed
        #     if int(self.current_sprite) >= len(self.sprites):
        #         self.current_sprite = 0
        #         self.attack_animation = False
        #
        # self.image = self.sprites[int(self.current_sprite)]

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Block(pygame.sprite.Sprite):
    """A class representing solid obstacles."""
    def __init__(self, color, rect):
        """The color is an (r,g,b) tuple; rect is a rect-style argument."""
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface(self.rect.size).convert()
        self.image.fill(color)
        self.type = "normal"


class Control(object):

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.keys = pygame.key.get_pressed()
        self.done = False
        self.player = Player(200, 875, 4, 'Daniel', 100, 3, 1)
        self.enemy = Player(100, 900, 4, 'Daniel', 100, 3, 1)
        self.game_over = False

        moving_sprites = pygame.sprite.Group()
        moving_sprites.add(self.player)
        moving_sprites.add(self.enemy)

        self.level = pygame.Surface((1000, 1000)).convert()
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

    def make_text(self):
        font = pygame.font.Font(None, 100)
        message = "You win. Celebrate."
        text = font.render(message, True, (100, 100, 175))
        rect = text.get_rect(centerx=self.level_rect.centerx, y=100)
        return text, rect

    def make_obstacles(self):
        floor = Block(pygame.Color("darkgreen"), (100, 980, 890, 10))
        static = []
        # (250, 780, 200, 100)
        top = 500
        for i in range(4):
            left = random.randint(100, 980)
            top += 100
            static.append(Block(pygame.Color("darkgreen"), (left, top, 200, 25)))
        return pygame.sprite.Group(floor, static)

    def update_viewport(self, speed):
        for i in (0, 1):
            first_third = self.viewport[i] + self.viewport.size[i] // 3
            second_third = first_third + self.viewport.size[i] // 3
            player_center = self.player.rect.center[i]
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
                if event.key == pygame.K_SPACE:
                    self.player.jump(self.obstacles)
                elif event.key == pygame.K_f:
                    self.player.jump(self.obstacles)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.jump_cut()
                elif event.key == pygame.K_f:
                    self.player.jump_cut()

    def update(self):
        self.keys = pygame.key.get_pressed()
        self.player.pre_update(self.obstacles)
        self.obstacles.update(self.player, self.obstacles)
        self.player.update(self.obstacles, self.keys)
        self.update_viewport(self.player.total_displacement)

    def draw(self):
        self.draw_bg()
        self.level.fill(pygame.Color("lightblue"), self.viewport)
        self.obstacles.draw(self.level)
        self.level.blit(self.win_text, self.win_rect)
        self.player.draw(self.level)
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

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))


    #function for drawing background
    def draw_bg(self):
        self.level.blit(self.background_img, (0, 0))


    def draw_panel(self, player1, player2, font, color):
        #draw panel rectangle
        screen.blit(self.panel_img, (0, screen_height - bottom_panel))
        #show knight stats
        self.draw_text(f'{player1.name} HP: {player1.health}', font, color, 100, screen_height - bottom_panel + 10)

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
