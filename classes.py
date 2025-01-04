import os
import sys

import pygame

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def change_board(self, new_board):
        '''изменяет поле. самостоятельно находит длину и ширину. поле должно быть прямоугольным,
         по краям должны быть стены,так как система туннелей отсутствует.'''
        self.board = new_board
        self.width = len(new_board[0])
        self.height = len(new_board)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                if self.board[j][i]:
                    kv = pygame.Rect(self.left + self.cell_size * i + 1, self.top + self.cell_size * j + 1,
                                     self.cell_size - 2,
                                     self.cell_size - 2)
                    pygame.draw.rect(screen, 'blue', kv, 0)

    def get_cell(self, pos):
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        return (x, y, self.board[y][x]) if (x >= 0 and x < self.width and y >= 0 and y < self.height) else None


class AbstractMob(pygame.sprite.Sprite):  # Движущиеся объекты
    def __init__(self, board, *group):
        super().__init__(*group)
        self.image = load_image(
            "Original_PacMan.png")  # временно для всех подвижных объектов будет использована эта картинка, просто чтобы видеть спрайт
        self.board = board
        self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.rect = self.image.get_rect()

    def stabilize_y(self):  # эта функция и следущая нужна для перестановки объекта по центру клетки
        ycell = self.board.get_cell((self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))[1]
        return ycell * self.board.cell_size + self.board.top

    def stabilize_x(self):  # эта функция и следущая нужна для перестановки объекта по центру клетки
        xcell = self.board.get_cell((self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))[0]
        return xcell * self.board.cell_size + self.board.left


class AbstractGhost(AbstractMob):  # призраки
    pass


class Ghost1(AbstractGhost):  # для каждого призрака нужен свой класс, тк в оригинале у них разные алгоритмы поиска пути
    pass


class Ghost2(AbstractGhost):
    pass


class Ghost3(AbstractGhost):
    pass


class Ghost4(AbstractGhost):
    pass


class Pacman(AbstractMob):  # пакман
    def __init__(self, screen, *group):
        super().__init__(screen, *group)
        self.rect = self.rect.move(self.board.left + self.board.cell_size, self.board.top + self.board.cell_size)
        self.napr = 'r'
        self.speed = 1

    def update(self, tick, napr):
        if napr is not None:
            self.napr = napr
        if tick == 0:
            pass
        elif self.napr == 'r' and not \
                self.board.get_cell(
                    (self.rect.x + self.rect.width + self.speed // tick, self.rect.y + self.rect.height // 2))[2]:
            self.rect = self.rect.move(self.speed // tick, 0)
            self.rect.y = self.stabilize_y()
        elif self.napr == 'l' and not \
        self.board.get_cell((self.rect.x - self.speed // tick, self.rect.y + self.rect.height // 2))[2]:
            self.rect = self.rect.move(self.speed // tick * -1, 0)
            self.rect.y = self.stabilize_y()
        elif self.napr == 'u' and not \
        self.board.get_cell((self.rect.x + self.rect.width // 2, self.rect.y - self.speed // tick))[2]:
            self.rect = self.rect.move(0, self.speed // tick * -1)
            self.rect.x = self.stabilize_x()
        elif self.napr == 'd' and not \
                self.board.get_cell(
                    (self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height + self.speed // tick))[2]:
            self.rect = self.rect.move(0, self.speed // tick)
            self.rect.x = self.stabilize_x()


class AbstractItem(pygame.sprite.Sprite):  # все неподвижные объекты
    pass


class Point(AbstractItem):  # точки, которые нужно собирать
    pass


class BigPoint(AbstractItem):  # таблетки, которые позволяют есть призраков
    pass


class Fruit(AbstractItem):  # фрукт, дающий больше очков
    pass
