from classes_and_functions import *

pygame.init()
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)

board = Board(10, 10)
board.set_view(0, 0, 40)

with open('data/levels') as f:  # 0 - пустота 1 - стена 2 - проход призраков
    text = f.read()
board.change_board([[int(j) for j in i.strip()] for i in text.split()])

with open('data/itemlevels') as f:  # 0 - пустота 1 - стена 2 - проход призраков
    text = f.read()
board.change_itemboard([[int(j) for j in i.strip()] for i in text.split()])

pm = pygame.sprite.Group()
ghosts = pygame.sprite.Group()
items = pygame.sprite.Group()

pacman = Pacman(board, pm)
Ghost1(board, ghosts)
Ghost2(board, ghosts)
Ghost3(board, ghosts)
Ghost4(board, ghosts)

clock = pygame.time.Clock()

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

    pm.draw(screen)
    pm.update(time, napr)

    ghosts.draw(screen)
    ghosts.update(time, (pacman.about()))

    pygame.display.flip()
pygame.quit()
