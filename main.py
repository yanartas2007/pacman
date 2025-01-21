import sys
from time import sleep

import pygame

from classes_and_functions import *

pygame.init()
size = width, height = 1000, 860
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def draw_intro():
    intro_text = ["", "                                           <<< PACMAN >>>", "", "",
                  "   !!! Правила игры !!!", "",
                  "   Управляйте пакманом", "   и избегайте встречи с привидениями.", "",
                  "   Для победы в игре соберите", "   все точки!", "", "", "", "", "   Нажмите, чтобы начать..."]

    fon = pygame.transform.scale(load_image('zastavka.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


draw_intro()

board = Board(10, 10)
board.set_view(0, 0, 40)
sleep(0.1)  # без этой строчки иногда не запускается, тк фпс первого кадра стремиться к бесконечности

with open('data/levels') as f:
    text = f.read()
board.change_board([[int(j) for j in i.strip()] for i in text.split()])

board.change_itemboard(12, 18)

pm = pygame.sprite.Group()
ghosts = pygame.sprite.Group()

pacman = Pacman(board, pm, coords=(12, 18))
Ghost1(board, ghosts, coords=(10, 9), pacman=pm)
Ghost2(board, ghosts, coords=(11, 9), pacman=pm)
Ghost3(board, ghosts, coords=(12, 9), pacman=pm)
Ghost4(board, ghosts, coords=(13, 9), pacman=pm)


def game_over():
    fon = pygame.transform.scale(load_image('gameover.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 50
    game_over_text = ["Количество набранных очков:"]
    for line in game_over_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
            pygame.display.flip()
            clock.tick(FPS)


lifes = 3
running = True
isfirst = True
score = 0
while running:
    napr = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                napr = 'l'
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                napr = 'r'
            elif event.key in (pygame.K_UP, pygame.K_w):
                napr = 'u'
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                napr = 'd'
    time = clock.tick()
    screen.fill('black')
    if isfirst:
        board.render(screen)
        pm.draw(screen)
        ghosts.draw(screen)
        load_score(screen, score, lifes)
        pygame.display.flip()
        if napr is None:
            continue
        else:
            isfirst = False
            pacman.napr = napr
            continue

    board.render(screen)
    score = board.score
    board.time += time
    board.update()
    load_score(screen, score, lifes)

    e = board.take_events()
    if len(e) != 0:
        for i in e:
            if i == 'BigPoint':
                for j in ghosts:
                    j.becomeblue()
            if i == 'PacmanDied':
                lifes -= 1
                board.time = 0
                sleep(1)  # эту строчку заменить на анимацию смерти
                if lifes == 0:
                    game_over()
                pm = pygame.sprite.Group()
                ghosts = pygame.sprite.Group()
                Ghost1(board, ghosts, coords=(10, 9), pacman=pm)
                Ghost2(board, ghosts, coords=(11, 9), pacman=pm)
                Ghost3(board, ghosts, coords=(12, 9), pacman=pm)
                Ghost4(board, ghosts, coords=(13, 9), pacman=pm)
                pacman = Pacman(board, pm, coords=(12, 18))
                sleep(1)
                isfirst = True

    pm.update(time, napr)
    pm.draw(screen)
    ghosts.update(time, (pacman.about()))
    ghosts.draw(screen)
    pygame.display.flip()

pygame.quit()
