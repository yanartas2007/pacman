import os
import random
import sys

import pygame

pygame.init()


def pacman_died():
    print('GAME OVER')
    sys.exit()


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
        return (int(x), int(y), self.board[int(y)][int(x)]) if (
                x >= 0 and x < self.width and y >= 0 and y < self.height) else None


class AbstractMob(pygame.sprite.Sprite):  # Движущиеся объекты
    def __init__(self, board, *group):
        super().__init__(*group)
        self.image = load_image(
            "Original_PacMan.png")
        self.board = board
        self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.rect = self.image.get_rect()
        self.x = self.rect.x  # координаты объекта могут выражаться как нецелое число, но его текстура всегда на целых координатах
        self.y = self.rect.y
        self.speed = self.board.cell_size / 675  # 25
        self.napr = 'r'

    def stabilize(self):
        '''без этой функции очень сложно попасть в проход в одну клетку. а еще если в результате ошибки обЪект окажется частично в стене, она вытолкнет его'''
        if self.board.get_cell(
                (self.rect.x + 1, self.rect.y + 1))[2] or self.board.get_cell(
            (self.rect.x + self.rect.width - 1, self.rect.y + 1))[2] or \
                self.board.get_cell((self.rect.x + 1, self.rect.y + self.rect.height - 1))[2] or \
                self.board.get_cell((self.rect.x + self.rect.width - 1, self.rect.y + self.rect.height - 1))[2]:
            self.y = self.board.get_cell((self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))[
                         1] * self.board.cell_size + self.board.top
            self.x = self.board.get_cell((self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))[
                         0] * self.board.cell_size + self.board.left

    def update_coords(self):
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def update(self, time, napr=None):
        tick = 1 / time
        if napr is not None:
            self.napr = napr
        if tick == 0:
            pass
        elif self.napr == 'r' and not \
                self.board.get_cell(
                    (self.rect.x + self.rect.width + self.speed // tick, self.rect.y + self.rect.height // 2))[2]:
            self.x += self.speed / tick

        elif self.napr == 'l' and not \
                self.board.get_cell(
                    (self.rect.x - self.speed // tick, self.rect.y + self.rect.height // 2))[2]:
            self.x -= self.speed / tick

        elif self.napr == 'u' and not \
                self.board.get_cell(
                    (self.rect.x + self.rect.width // 2, self.rect.y - self.speed // tick))[2]:
            self.y -= self.speed / tick

        elif self.napr == 'd' and not \
                self.board.get_cell(
                    (self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height + self.speed // tick))[2]:
            self.y += self.speed / tick

        self.stabilize()
        self.update_coords()

    def about(self):
        return (*self.board.get_cell((self.x + self.rect.width // 2, self.y + self.rect.height // 2))[:-1], self.napr)


class AbstractGhost(AbstractMob):  # призраки
    def __init__(self, screen, *group):
        super().__init__(screen, *group)
        self.update_coords()
        self.speed *= 0.8
        self.napr = 'r'
        self.x = self.board.left + self.board.cell_size * 10
        self.y = self.board.top + self.board.cell_size * 10

    def targeting(self, target=(1, 1, 'r')):  # поиск пути
        x, y = self.board.get_cell((self.x + self.rect.width // 2, self.y + self.rect.height // 2))[:-1]
        x, y = int(x), int(y)

        if x == target[0] and y == target[1]:
            pacman_died()

        bcopy = [['#' if self.board.board[i][j] == 1 else ' ' for j in range(len(self.board.board[i]))] for i in
                 range(len(self.board.board))]
        bcopy[target[1]][target[0]] = 0
        bcopy[y][x] = '***'

        flag = 0
        for i in range(1, 50):
            for n in range(1, len(self.board.board) - 1):
                for f in range(1, len(self.board.board[n]) - 1):
                    if i - 1 in (bcopy[n - 1][f], bcopy[n][f - 1], bcopy[n + 1][f], bcopy[n][f + 1]) and bcopy[n][
                        f] == ' ':
                        bcopy[n][f] = i
                    if bcopy[n][f] == '***':
                        if str(bcopy[n - 1][f]).isdigit():
                            napr = 'u'
                        elif str(bcopy[n + 1][f]).isdigit():
                            napr = 'd'
                        elif str(bcopy[n][f - 1]).isdigit():
                            napr = 'l'
                        elif str(bcopy[n][f + 1]).isdigit():
                            napr = 'r'
                        else:
                            continue
                        flag = 1
                        break
                if flag:
                    break
            if flag:
                break
        else:
            return random.choice(('l', 'r', 'u', 'd'))
        return napr

    def hide(self):  # функия рассеивания, альтарнативная модель поведения
        pass

    def update(self, time, target=(1, 1, 'r')):  # вместо направления получает цель и сам преобразует в направление
        napr = self.targeting(target)
        super().update(time, napr)


class Ghost1(AbstractGhost):
    def __init__(self, screen, *group):
        super().__init__(screen, *group)
        self.x = self.board.left + self.board.cell_size * 10
        self.y = self.board.top + self.board.cell_size * 10
        self.update_coords()


class Ghost2(AbstractGhost):
    def __init__(self, screen, *group):
        super().__init__(screen, *group)
        self.x = self.board.left + self.board.cell_size * 11
        self.y = self.board.top + self.board.cell_size * 10
        self.update_coords()


class Ghost3(AbstractGhost):
    def __init__(self, screen, *group):
        super().__init__(screen, *group)
        self.x = self.board.left + self.board.cell_size * 12
        self.y = self.board.top + self.board.cell_size * 10
        self.update_coords()


class Ghost4(AbstractGhost):
    def __init__(self, screen, *group):
        super().__init__(screen, *group)
        self.x = self.board.left + self.board.cell_size * 13
        self.y = self.board.top + self.board.cell_size * 10
        self.update_coords()


class Pacman(AbstractMob):  # пакман
    def __init__(self, screen, *group):
        super().__init__(screen, *group)
        self.x = self.board.left + self.board.cell_size
        self.y = self.board.top + self.board.cell_size
        self.update_coords()
        self.napr = 'r'


class AbstractItem(pygame.sprite.Sprite):  # все неподвижные объекты
    pass


class Point(AbstractItem):  # точки, которые нужно собирать
    pass


class BigPoint(AbstractItem):  # таблетки, которые позволяют есть призраков
    pass


class Fruit(AbstractItem):  # фрукт, дающий больше очков
    pass
