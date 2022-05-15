#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import pygame, sys
import game

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Fight Knight')
screen = pygame.display.set_mode((800, 550), 0, 32)
background_img = pygame.image.load('img/Background/background.png').convert_alpha()

font = pygame.font.SysFont(None, 20)

def draw_bg():
    screen.blit(background_img, (0, 0))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False


def main_menu():
    while True:
        draw_bg()
        draw_text('MAIN MENU', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 100, 200, 50)

        button_2 = pygame.Rect(50, 200, 200, 50)

        button_3 = pygame.Rect(50, 300, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                game.Control().mainloop()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        pygame.draw.rect(screen, (51, 51, 0), button_1)
        screen.blit(font.render('Start', True, (255,0,0)), (100, 120))
        pygame.draw.rect(screen, (51, 51, 0), button_2)
        screen.blit(font.render('Options', True, (255,0,0)), (100, 220))
        pygame.draw.rect(screen, (51, 51, 0), button_3)
        screen.blit(font.render('Character select', True, (255,0,0)), (100, 320))

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


# def game():
#     running = True
#     while running:
#         draw_bg()
# #         screen.fill((0, 0, 0))
#         draw_text('game', font, (255, 255, 255), screen, 20, 20)
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     running = False
#
#         pygame.display.update()
#         mainClock.tick(60)


def options():
    running = True
    while running:
        screen.fill((0, 0, 0))

        draw_text('options', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


main_menu()