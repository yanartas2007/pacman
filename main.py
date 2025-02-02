import sys

import pygame.sprite

from classes_and_functions import *

pygame.init()
size = width, height = 1000, 860
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()

debug_load()

draw_intro(screen)

board = Board(10, 8)
board.set_view(0, 0, 100)
sleep(0.1)  # без этой строчки иногда не запускается, тк фпс первого кадра стремиться к бесконечности

with open('data/level_1') as f:
    text = f.read()
board.change_board([[int(j) for j in i.strip()] for i in text.split()])

board.change_itemboard(1, 1)

pm = pygame.sprite.Group()
ghosts = pygame.sprite.Group()

pacman = Pacman(board, pm, coords=(1, 1))
Ghost1(board, ghosts, coords=(8, 6), pacman=pm)

close_intro(screen, board, ghosts, pm)
lifes = 3
if debug_dict['inflives']:
    lifes += 1000
lifeparticles = pygame.sprite.Group()
lifeslist = []
for i in range(lifes):
    e = PacmanLifeParticle(board, lifeparticles, number=i)
    lifeslist.append(e)
running = True
isfirst = True
level = 1
score = 0
scorewithlastbonus = 0

pause = False

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
            elif event.key in (pygame.K_SPACE, pygame.K_F1):
                pause = True if pause == False else False
    time = clock.tick()
    screen.fill('black')
    if pause:
        board.render(screen)
        pm.draw(screen)
        ghosts.draw(screen)
        lifeparticles.draw(screen)
        load_score(screen, score)
        font = pygame.font.Font(None, 200)
        text = font.render('pause', True, (0, 255, 0))
        text_x = width // 2 - 200
        text_y = height // 2 - 100
        screen.blit(text, (text_x, text_y))
        font = pygame.font.Font(None, 50)
        text = font.render('click F1 or Space', True, (0, 255, 0))
        text_x = width // 2 - 200
        text_y = height // 2 +100
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()
        continue
    if isfirst:  # в начале, пакман неподвижен, ничего не происходит до первого нажатия
        if debug_dict['noghosts']:
            ghosts = pygame.sprite.Group()
        board.render(screen)
        pm.draw(screen)
        ghosts.draw(screen)
        lifeparticles.draw(screen)
        load_score(screen, score)
        pygame.display.flip()
        if napr is None:
            continue
        else:
            isfirst = False
            pacman.napr = napr
            continue

    board.render(screen)
    score = board.score
    if score - scorewithlastbonus >= 3000:
        lifes += 1
        e = PacmanLifeParticle(board, lifeparticles, number=lifes - 1)
        lifeslist.append(e)
        scorewithlastbonus += 3000
    board.time += time
    board.update()
    load_score(screen, score)

    e = board.take_events()
    if len(e) != 0:
        for i in e:
            if i == 'BigPoint':  # таблетка съедена
                for j in ghosts:
                    j.becomeblue()
            if i == 'PacmanDied':  # пакман умер
                playmusic('data/gameover.mp3')
                lifes -= 1
                lifeslist[-1].kill()
                lifeslist = lifeslist[:-1]
                if lifes == 0:
                    open_gameover(screen, board, ghosts, pm)
                    game_over(board.score)
                elif level == 3:
                    board.time = 0
                    pacmandeathanimation(screen, board, pacman, pm, ghosts)
                    pm = pygame.sprite.Group()
                    ghosts = pygame.sprite.Group()
                    Ghost1(board, ghosts, coords=(10, 9), pacman=pm)
                    Ghost2(board, ghosts, coords=(11, 9), pacman=pm)
                    Ghost3(board, ghosts, coords=(12, 9), pacman=pm)
                    Ghost4(board, ghosts, coords=(13, 9), pacman=pm)
                    pacman = Pacman(board, pm, coords=(12, 18))
                    sleep(0.6)
                    isfirst = True
                elif level == 2:
                    board.time = 0
                    pacmandeathanimation(screen, board, pacman, pm, ghosts)
                    pm = pygame.sprite.Group()
                    ghosts = pygame.sprite.Group()
                    Ghost4(board, ghosts, coords=(3, 3), pacman=pm)
                    Ghost2(board, ghosts, coords=(4, 3), pacman=pm)
                    Ghost3(board, ghosts, coords=(5, 3), pacman=pm)
                    pacman = Pacman(board, pm, coords=(5, 10))
                    sleep(0.6)
                    isfirst = True
                elif level == 1:
                    board.time = 0
                    pacmandeathanimation(screen, board, pacman, pm, ghosts)
                    pm = pygame.sprite.Group()
                    ghosts = pygame.sprite.Group()
                    pacman = Pacman(board, pm, coords=(1, 1))
                    Ghost1(board, ghosts, coords=(8, 6), pacman=pm)
                    sleep(0.6)
                    isfirst = True
            if i == 'NEXTLEVEL' and level == 1:  # переход н 2 уровень
                level = 2
                playmusic('data/win.mp3')
                board = Board(10, 8, board.score)
                board.set_view(0, 0, 67)
                with open('data/level_2') as f:
                    text = f.read()
                board.change_board([[int(j) for j in i.strip()] for i in text.split()])
                board.change_itemboard(5, 10)
                pm = pygame.sprite.Group()
                ghosts = pygame.sprite.Group()
                Ghost4(board, ghosts, coords=(3, 3), pacman=pm)
                Ghost2(board, ghosts, coords=(4, 3), pacman=pm)
                Ghost3(board, ghosts, coords=(5, 3), pacman=pm)
                pacman = Pacman(board, pm, coords=(5, 10))
                isfirst = True
            elif i == 'NEXTLEVEL' and level == 2:  # переход на 3 уровень
                level = 3
                playmusic('data/win.mp3')
                board = Board(10, 8, board.score)
                board.set_view(0, 0, 40)
                with open('data/level_3') as f:
                    text = f.read()
                board.change_board([[int(j) for j in i.strip()] for i in text.split()])
                board.change_itemboard(12, 18)
                pm = pygame.sprite.Group()
                ghosts = pygame.sprite.Group()
                Ghost1(board, ghosts, coords=(10, 9), pacman=pm)
                Ghost2(board, ghosts, coords=(11, 9), pacman=pm)
                Ghost3(board, ghosts, coords=(12, 9), pacman=pm)
                Ghost4(board, ghosts, coords=(13, 9), pacman=pm)
                pacman = Pacman(board, pm, coords=(12, 18))
                isfirst = True
            if i == 'WIN':
                open_win(screen, board, ghosts, pm)
                pacman_win(score)

    pm.update(time, napr)
    pm.draw(screen)
    ghosts.update(time, (pacman.about()))
    ghosts.draw(screen)
    lifeparticles.draw(screen)
    lifeparticles.update(time)
    pygame.display.flip()

pygame.quit()
