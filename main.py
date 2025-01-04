from classes import *


pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)

board = Board(10, 10)
board.set_view(0, 0, 50)
board.change_board([list(map(int, list('1111111111'))),  # лучше хранить в txt или csv, пока так
                    list(map(int, list('1000000001'))),
                    list(map(int, list('1011101101'))),
                    list(map(int, list('1010000101'))),
                    list(map(int, list('1000110101'))),
                    list(map(int, list('1010100101'))),
                    list(map(int, list('1010000101'))),
                    list(map(int, list('1010110101'))),
                    list(map(int, list('1000110001'))),
                    list(map(int, list('1111111111')))])

pm = pygame.sprite.Group()
ghosts = pygame.sprite.Group()
items = pygame.sprite.Group()

Pacman(board, pm)

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
    board.render(screen)
    pm.draw(screen)
    pm.update(clock.tick(), napr)
    pygame.display.flip()
pygame.quit()
