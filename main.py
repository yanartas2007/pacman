from classes_and_functions import *

pygame.init()
size = width, height = 1000, 860
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()

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
lifeparticles = pygame.sprite.Group()
lifeslist = []
for i in range(lifes):
    e = PacmanLifeParticle(board, lifeparticles, number=i)
    lifeslist.append(e)
running = True
isfirst = True
level = 1
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
            elif event.key == pygame.K_F1 and DEBUG:  # далее - кнопки отладки. по умолчанию выключены
                board.events = []
                board.level = -1
                board.next_level()
                level = 1
            elif event.key == pygame.K_F2 and DEBUG:
                board.events = []
                board.level = 0
                board.next_level()
                level = 2
            elif event.key == pygame.K_F3 and DEBUG:
                board.events = []
                board.level = 1
                board.next_level()
                level = 3
            elif event.key == pygame.K_F5 and DEBUG:
                e = PacmanLifeParticle(board, lifeparticles, number=len(lifeslist))
                lifeslist.append(e)
                lifes += 1
            elif event.key == pygame.K_F6 and DEBUG:
                lifes = 1
                open_gameover(screen, board, ghosts, pm)
                game_over(board.score)
            elif event.key == pygame.K_F7 and DEBUG:
                open_win(screen, board, ghosts, pm)
                pacman_win(board.score)
            elif event.key == pygame.K_F8 and DEBUG:
                ghosts = pygame.sprite.Group()
            elif event.key == pygame.K_F9 and DEBUG:
                score += 1000
    time = clock.tick()
    screen.fill('black')
    if isfirst:  # в начале, пакман неподвижен, ничего не происходит до первого нажатия
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
            if i == 'NEXTLEVEL2':  # переход н 2 уровень
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
            if i == 'NEXTLEVEL3':  # переход на 3 уровень
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
            if i == 'NEXTLEVEL1':  # переход на 1 уровень (только для отладки)
                level = 1
                playmusic('data/win.mp3')
                board = Board(10, 8, board.score)
                board.set_view(0, 0, 100)

                with open('data/level_1') as f:
                    text = f.read()
                board.change_board([[int(j) for j in i.strip()] for i in text.split()])

                board.change_itemboard(1, 1)

                pm = pygame.sprite.Group()
                ghosts = pygame.sprite.Group()

                pacman = Pacman(board, pm, coords=(1, 1))
                Ghost1(board, ghosts, coords=(8, 6), pacman=pm)
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
