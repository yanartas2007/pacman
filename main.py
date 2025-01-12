from time import sleep

from classes_and_functions import *

pygame.init()
size = width, height = 1000, 860
screen = pygame.display.set_mode(size)

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

clock = pygame.time.Clock()
lifes = 3

running = True
while running:
    napr = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                napr = 'l'
            elif event.key == pygame.K_RIGHT:
                napr = 'r'
            elif event.key == pygame.K_UP:
                napr = 'u'
            elif event.key == pygame.K_DOWN:
                napr = 'd'
    screen.fill('black')
    time = clock.tick()

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

    pm.draw(screen)
    pm.update(time, napr)

    ghosts.draw(screen)
    ghosts.update(time, (pacman.about()))

    pygame.display.flip()
pygame.quit()
