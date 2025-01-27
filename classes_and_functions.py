import os
import random
import sys

import pygame

pygame.init()

ANIMATIONSPEED = 100  # чем меньше тем быстрее меняется
FPS = 50
DEBUG = False # отладка. если заменить на True, f1 f2 f3 переключение уровней f5 + жизнь f6 проигрыш f7 выигрыш
pygame.init()
size = width, height = 1000, 860
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()



def terminate(): # завершение
    pygame.quit()
    sys.exit()

def draw_intro(screen):
    file = 'intro.mp3'
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    # интро
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
def game_over(score):
    # вывод окна проигрыша
    fon = pygame.transform.scale(load_image('gameover.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 50
    game_over_text = ["Количество набранных очков:", str(score)]
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
                    terminate()
            pygame.display.flip()
            clock.tick(FPS)

def pacman_win(score): # вывод окна выигрыша
    win_text = ["Количество набранных очков:", str(score)]
    fon = pygame.transform.scale(load_image('win.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in win_text:
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
                    terminate()
            pygame.display.flip()
            clock.tick(FPS)



def load_image(name, colorkey=None): # загрузка изображения
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


def load_score(screen, score, lifes): # показывает очки и жизни
    font = pygame.font.Font(None, 50)
    text = font.render(f"score: {score}", True, (255, 255, 255))
    text_x = 700
    text_y = 810
    screen.blit(text, (text_x, text_y))

    for i in range(lifes):
        image = load_image("Original_PacMan.png", -1)
        image1 = pygame.transform.scale(image, (40, 40))
        screen.blit(image1, (100 + i * 50,
                             810))


class Board: # Доска
    def __init__(self, width, height, score=0):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(
            height)]  # 0 - пустота 1 - стена 2 - проход призраков 3 - не отображается, место без предметов 4 - туннель
        self.itemboard = [[0] * width for _ in range(height)]  # 1 - точка 2 - фрукт 3 - большая точка
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.points = 0
        self.fruits = 0
        self.score = score
        self.time = 0
        self.events = []
        self.clr1 = 100
        self.clr2 = 100
        self.clr3 = 255
        self.clrchange = 3
        self.level = 1

    def change_board(self, new_board): # Смена доски
        '''изменяет поле. самостоятельно находит длину и ширину. поле должно быть прямоугольным,
         по краям должны быть стены,так как система туннелей отсутствует.'''
        self.board = new_board
        self.width = len(new_board[0])
        self.height = len(new_board)

    def change_itemboard(self, x, y): # расставляет точки для сбора везде, куда можно попасть
        self.itemboard = [[0] * self.width for _ in range(self.height)]
        bcopy = [['#' if self.board[i][j] != 0 else ' ' for j in range(len(self.board[i]))] for i in
                 range(len(self.board))]
        bcopy[y][x] = '*'
        for i in range(1, 50):
            for n in range(len(self.board)):
                for f in range(len(self.board[n])):
                    t = []

                    if n != 0:
                        t.append(bcopy[n - 1][f])
                    if n != len(self.board) - 1:
                        t.append(bcopy[n + 1][f])
                    if f != 0:
                        t.append(bcopy[n][f - 1])
                    if f != len(self.board[n]) - 1:
                        t.append(bcopy[n][f + 1])

                    if ('*' in t and
                            bcopy[n][f] == ' '):
                        bcopy[n][f] = '*'
                        self.itemboard[n][f] = 1
                        self.points += 1
        bigpoints = 0
        while bigpoints < self.points // 20 + 1:
            randompoint = (
                random.randint(1, len(self.board[0]) - 1), random.randint(1, len(self.board) - 1))
            if self.itemboard[randompoint[1]][randompoint[0]] == 1 and self.board[randompoint[1]][
                randompoint[0]] == 0:
                self.itemboard[randompoint[1]][randompoint[0]] = 3
                bigpoints += 1

    def set_view(self, left, top, cell_size): # смена параметров отображения
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen): # показывает вместе стены и предметы
        self.renderwalls(screen)
        self.renderitems(screen)

    def renderwalls(self, screen): # показывает стены
        if self.clrchange == 3:
            self.clr3 -= 1
            self.clr2 += 1
            if self.clr2 == 140 or self.clr3 == 0:
                self.clrchange = 2
        elif self.clrchange == 2:
            self.clr2 -= 1
            self.clr1 += 1
            if self.clr1 == 140 or self.clr2 == 0:
                self.clrchange = 1
        else:
            self.clr1 -= 1
            self.clr3 += 1
            if self.clr3 == 255 or self.clr1 == 0:
                self.clrchange = 3

        for i in range(self.width):
            for j in range(self.height):
                if self.board[j][i] == 1:
                    kv = pygame.Rect(self.left + self.cell_size * i + 1, self.top + self.cell_size * j + 1,
                                     self.cell_size - 2,
                                     self.cell_size - 2)
                    pygame.draw.rect(screen, (self.clr1, self.clr2, self.clr3), kv, 0)
                elif self.board[j][i] == 2:
                    kv = pygame.Rect(self.left + self.cell_size * i + 1, self.top + self.cell_size * j + 1,
                                     self.cell_size,
                                     self.cell_size // 4)
                    pygame.draw.rect(screen, 'red', kv, 0)

    def renderitems(self, screen): # показывает предметы
        for i in range(self.width):
            for j in range(self.height):
                if self.itemboard[j][i] == 1:
                    kv = pygame.Rect(self.left + self.cell_size * i + 1 + self.cell_size // 2,
                                     self.top + self.cell_size * j + 1 + self.cell_size // 2,
                                     self.cell_size // 10,
                                     self.cell_size // 10)
                    pygame.draw.rect(screen, 'white', kv, 0)
                if self.itemboard[j][i] == 2:
                    image = load_image("fruit.png", -1)
                    image1 = pygame.transform.scale(image, (self.cell_size, self.cell_size))
                    screen.blit(image1, (self.left + self.cell_size * i + 1,
                                         self.top + self.cell_size * j + 1))
                if self.itemboard[j][i] == 3:
                    kv = pygame.Rect(self.left + self.cell_size * i + 1 + self.cell_size // 4,
                                     self.top + self.cell_size * j + 1 + self.cell_size // 4,
                                     self.cell_size // 2,
                                     self.cell_size // 2)
                    pygame.draw.rect(screen, 'white', kv, 0)

    def getitem(self, pos): # возвращает предмет в клетке, где пакман
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        if self.itemboard[int(y)][int(x)] == 1:
            self.itemboard[int(y)][int(x)] = 0
            self.points -= 1
            self.score += 10
        if self.itemboard[int(y)][int(x)] == 2:
            self.itemboard[int(y)][int(x)] = 0
            self.score += random.choice((100, 150, 200, 250, 300))
            self.fruits -= 1
        if self.itemboard[int(y)][int(x)] == 3:
            self.itemboard[int(y)][int(x)] = 0
            self.points -= 1
            self.score += 50
            self.events.append('BigPoint')

    def update(self): # обновляет поле
        if self.points == 0:
            if self.level == 3:
                pacman_win(self.score)
            else:
                self.next_level()

        if self.time >= 35000:
            if self.fruits >= 3:
                self.time = 0
                return
            for i in range(3):
                randompoint = (
                    random.randint(1, len(self.board[0]) - 1), random.randint(1, len(self.board) - 1))
                if self.itemboard[randompoint[1]][randompoint[0]] == 0 and self.board[randompoint[1]][
                    randompoint[0]] == 0:
                    self.itemboard[randompoint[1]][randompoint[0]] = 2
                    self.fruits += 1
                    break
            self.time = 0

    def get_cell(self, pos): # возвращает клетку
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        return (int(x), int(y), self.board[int(y)][int(x)]) if (
                x >= 0 and x < self.width and y >= 0 and y < self.height) else None


    def take_events(self): # возвращает список произошедших событий
        a = self.events[:]
        self.events = []
        return a

    def next_level(self): # переключает уровень на следующий
        self.level += 1
        self.points = 0
        self.events.append(f'NEXTLEVEL{self.level}')


class AbstractMob(pygame.sprite.Sprite):  # Движущиеся объекты
    def __init__(self, board, *group, coords):
        super().__init__(*group)
        self.images = []
        self.board = board
        self.images.append(pygame.transform.scale(pygame.image.load('data/r1.png'), (self.board.cell_size, self.board.cell_size)))
        self.images.append(pygame.transform.scale(pygame.image.load('data/r2.png'), (self.board.cell_size, self.board.cell_size)))
        self.images.append(pygame.transform.scale(pygame.image.load('data/r3.png'), (self.board.cell_size, self.board.cell_size)))
        self.images.append(pygame.transform.scale(pygame.image.load('data/r4.png'), (self.board.cell_size, self.board.cell_size)))
        self.images.append(pygame.transform.scale(pygame.image.load('data/r5.png'), (self.board.cell_size, self.board.cell_size)))
        self.images.append(pygame.transform.scale(pygame.image.load('data/r6.png'), (self.board.cell_size, self.board.cell_size)))
        self.index = 0
        self.image = self.images[self.index]
        self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.rect = self.image.get_rect()
        self.x = self.rect.x  # координаты объекта могут выражаться как нецелое число, но его текстура всегда на целых координатах
        self.y = self.rect.y
        self.speed = self.board.cell_size / 675  # 25
        self.napr = 'r'
        self.x = self.board.left + self.board.cell_size * coords[0]
        self.y = self.board.top + self.board.cell_size * coords[1]
        self.timetochangeimage = 0

    def updateanimation(self, tick):
        if self.timetochangeimage > ANIMATIONSPEED:
            self.timetochangeimage = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
        else:
            self.timetochangeimage += tick

        if self.napr == 'r':
            self.image = self.images[self.index]
        elif self.napr == 'd':
            self.image = pygame.transform.rotate(self.images[self.index], -90)
        elif self.napr == 'u':
            self.image = pygame.transform.rotate(self.images[self.index], 90)
        elif self.napr == 'l':
            self.image = pygame.transform.flip(self.images[self.index], True, False)

    def stabilize(self):
        '''без этой функции очень сложно попасть в проход в одну клетку. а еще если в результате ошибки обЪект окажется частично в стене, она вытолкнет его'''
        if self.board.get_cell(
                (self.rect.x + 1, self.rect.y + 1))[2] == 1 or self.board.get_cell(
            (self.rect.x + self.rect.width - 1, self.rect.y + 1))[2] == 1 or \
                self.board.get_cell((self.rect.x + 1, self.rect.y + self.rect.height - 1))[2] == 1 or \
                self.board.get_cell((self.rect.x + self.rect.width - 1, self.rect.y + self.rect.height - 1))[2] == 1:
            self.y = self.board.get_cell((self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))[
                         1] * self.board.cell_size + self.board.top
            self.x = self.board.get_cell((self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))[
                         0] * self.board.cell_size + self.board.left

    def update_coords(self): # перемещает картинку в место реального нахождения
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
                    (self.rect.x + self.rect.width + self.speed // tick, self.rect.y + self.rect.height // 2))[2] == 1:
            self.x += self.speed / tick


        elif self.napr == 'l' and not \
                self.board.get_cell(
                    (self.rect.x - self.speed // tick, self.rect.y + self.rect.height // 2))[2] == 1:
            self.x -= self.speed / tick


        elif self.napr == 'u' and not \
                self.board.get_cell(
                    (self.rect.x + self.rect.width // 2, self.rect.y - self.speed // tick))[2] == 1:
            self.y -= self.speed / tick

        elif self.napr == 'd' and not \
                self.board.get_cell(
                    (self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height + self.speed // tick))[2] == 1:
            self.y += self.speed / tick

        self.stabilize()
        self.update_coords()

    def about(self): # возвращает позицию и направление
        return (*self.board.get_cell((self.x + self.rect.width // 2, self.y + self.rect.height // 2))[:-1], self.napr)


class AbstractGhost(AbstractMob):  # призраки
    def __init__(self, screen, *group, coords, pacman):
        super().__init__(screen, *group, coords=coords)
        self.image = load_image(
            "ghost.png", -1)  # картинка как заглушка
        self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.update_coords()
        self.speed *= 0.8
        self.napr = 'r'
        self.mode = 2  # 1 - преследование 0 - рассеивание 2 - ожидание 3 - синий 4 - глаза
        self.mtime = 0
        self.randompoint = None
        self.timechangemodel = 30000
        self.respawntime = 0
        self.runtime = 0
        self.pacman = pacman
        self.spawnpoint = (self.about()[0], self.about()[1], None)

    def targeting(self, target=(1, 1, 'r')):  # поиск пути, основан на волновом алгоритме
        x, y = self.board.get_cell((self.x + self.rect.width // 2, self.y + self.rect.height // 2))[:-1]
        x, y = int(x), int(y)

        bcopy = [['#' if self.board.board[i][j] == 1 else ' ' for j in range(len(self.board.board[i]))] for i in
                 range(len(self.board.board))]
        try:
            bcopy[target[1]][target[0]] = 0
        except IndexError:
            return None
        bcopy[y][x] = '***'

        flag = 0
        napr = None
        for i in range(1, 50):
            for n in range(len(self.board.board)):
                for f in range(len(self.board.board[n])):
                    t = []

                    if n != 0:
                        t.append(bcopy[n - 1][f])
                    else:
                        t.append(bcopy[self.board.height - 1][f])
                    if n != self.board.height - 1:
                        t.append(bcopy[n + 1][f])
                    else:
                        t.append(bcopy[0][f])
                    if f != 0:
                        t.append(bcopy[n][f - 1])
                    else:
                        t.append(bcopy[n][self.board.width - 1])
                    if f != self.board.width - 1:
                        t.append(bcopy[n][f + 1])
                    else:
                        t.append(bcopy[n][0])

                    if (i - 1 in t) and bcopy[n][f] == ' ':
                        bcopy[n][f] = i
                    if bcopy[n][f] == '***':
                        try:
                            if str(bcopy[n - 1][f]).isdigit():
                                napr = 'u'
                        except Exception:
                            if str(bcopy[self.board.height - 1][f]).isdigit():
                                napr = 'u'
                        try:
                            if str(bcopy[n + 1][f]).isdigit():
                                napr = 'd'
                        except Exception:
                            if str(bcopy[0][f]).isdigit():
                                napr = 'd'
                        try:
                            if str(bcopy[n][f - 1]).isdigit():
                                napr = 'l'
                        except Exception:
                            if str(bcopy[n][self.board.width - 1]).isdigit():
                                napr = 'l'
                        try:
                            if str(bcopy[n][f + 1]).isdigit():
                                napr = 'r'
                        except Exception:
                            if str(bcopy[n][0]).isdigit():
                                napr = 'r'
                        if napr is None:
                            continue
                        else:
                            flag = 1
                            break
                if flag:
                    break
            if flag:
                break
        else:
            return None
        return napr

    def update(self, time, target=(1, 1, 'r')):
        napr = None
        if self.mode == 2:
            if self.mtime < self.respawntime:
                self.mtime += time
            else:
                self.mtime = 0
                self.mode = 1
            return
        elif self.mode == 3:
            if self.runtime == 0:
                self.mtime = 0
                self.runtime = 20000
                self.image = load_image(
                    "fruit.png", -1)  # картинка как заглушка
                self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
            if self.mtime < self.runtime:
                self.mtime += time
                while 1:
                    runpoint = self.findrunpoint(target)
                    if runpoint is not None:
                        break
                napr = self.targeting((runpoint[0], runpoint[1], None))
            else:
                self.image = load_image(
                    "ghost.png", -1)  # картинка как заглушка
                self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
                self.runtime = 0
                self.mode = 1
                self.stabilize()
        elif self.mode == 4:
            napr = self.targeting(self.spawnpoint)
            if self.about()[:-1] == self.spawnpoint[:-1]:
                self.mode = 2
                self.image = load_image(
                    "ghost.png", -1)  # картинка как заглушка
                self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
                self.mtime = 0
                self.respawntime = 30000
        elif self.mtime > 30000 and random.randint(0, 10) == 5:
            self.mode = 0
            self.mtime = 0
        elif self.mode == 1:
            napr = self.targeting(target)
        elif self.mode == 0:
            if self.randompoint == None:
                self.randompoint = (
                    random.randint(1, len(self.board.board) - 1), random.randint(1, len(self.board.board[0]) - 1), None)
                while self.targeting(self.randompoint) == None:
                    self.randompoint = (
                        random.randint(1, len(self.board.board) - 1), random.randint(1, len(self.board.board[0]) - 1),
                        None)
            if abs(self.about()[0] - self.randompoint[0]) <= 1 and abs(
                    self.about()[1] - self.randompoint[1]) <= 1:
                self.randompoint = None
                self.mode = 1
                self.mtime = 0
                self.timechangemodel = random.randint(10000, 50000)
                napr = self.targeting(target)
            else:
                napr = self.targeting(self.randompoint)

        self.mtime += time
        super().update(time, napr)

        if pygame.sprite.spritecollideany(self, self.pacman):
            if self.mode in (0, 1):
                self.board.events.append('PacmanDied')
            if self.mode == 3:
                self.mode = 4
                self.board.score += 200
                self.image = load_image(
                    "Original_PacMan.png", -1)  # картинка как заглушка
                self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))

    def becomeblue(self): # когда пакман съедает таблетку
        if self.mode in (1, 0):
            self.mode = 3
            self.runtime = 0
            self.mtime = 0

    def findrunpoint(self, target): # находит точку, что бы убежать от пакмана
        bcopy = [['#' if self.board.board[i][j] == 1 else ' ' for j in range(len(self.board.board[i]))] for i in
                 range(len(self.board.board))]
        try:
            bcopy[target[1]][target[0]] = '#'
            if bcopy[target[1] + 1][target[0]] == ' ':
                bcopy[target[1] + 1][target[0]] = 0
            if bcopy[target[1] - 1][target[0]] == ' ':
                bcopy[target[1] - 1][target[0]] = 0
            if bcopy[target[1]][target[0] + 1] == ' ':
                bcopy[target[1]][target[0] + 1] = 0
            if bcopy[target[1]][target[0] - 1] == ' ':
                bcopy[target[1]][target[0] - 1] = 0
        except IndexError:
            return None

        maxx = 0
        maxy = 0
        for i in range(1, 50):
            for n in range(1, len(self.board.board) - 1):
                for f in range(1, len(self.board.board[n]) - 1):
                    if (i - 1 in (bcopy[n - 1][f], bcopy[n][f - 1], bcopy[n + 1][f], bcopy[n][f + 1]) and
                            bcopy[n][f] == ' '):
                        bcopy[n][f] = i
                        maxi = i
                        maxx = f
                        maxy = n
        return maxx, maxy

    def ghost_run_animation(self): # ЗДЕСЬ НУЖНО ЗАМЕНИТЬ НАЗВАНИЯ КАРТИНОК НА СИНИЕ
        if self.napr == 'l':
            self.image = load_image(
                "ldg.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'u':
            self.image = load_image(
                "udg.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'r':
            self.image = load_image(
                "rdg.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'd':
            self.image = load_image(
                "ddg.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))

    def ghost_eyes_animation(self): # ЗДЕСЬ НУЖНО ЗАМЕНИТЬ НАЗВАНИЯ КАРТИНОК НА ГЛАЗА(БЕЛЫЕ)
        if self.napr == 'l':
            self.image = load_image(
                "wgl.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'u':
            self.image = load_image(
                "wgu.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'r':
            self.image = load_image(
                "wgr.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'd':
            self.image = load_image(
                "wgd.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))

class Ghost1(AbstractGhost):
    def __init__(self, screen, *group, coords, pacman):
        super().__init__(screen, *group, coords=coords, pacman=pacman)
        self.image = load_image(
            "rgr.png", -1)
        self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.update_coords()
        self.speed *= 0.9
        self.respawntime = 1000

    def red_ghost_animation(self):
        if self.napr == 'l':
            self.image = load_image(
                "rgl.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'u':
            self.image = load_image(
                "rgu.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'r':
            self.image = load_image(
                "rgr.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'd':
            self.image = load_image(
                "rgd.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))

    def update(self, time, target):
        if self.mode == 3:
            self.ghost_run_animation()
        elif self.mode == 4:
            self.ghost_eyes_animation()
        else:
            self.red_ghost_animation()
        super().update(time, target)


class Ghost2(AbstractGhost):
    def __init__(self, screen, *group, coords, pacman):
        super().__init__(screen, *group, coords=coords, pacman=pacman)
        self.image = load_image(
            "pgr.png", -1)
        self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.update_coords()
        self.speed *= 0.8
        self.respawntime = 8000

    def pink_ghost_animation(self):
        if self.napr == 'l':
            self.image = load_image(
                "pgl.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'u':
            self.image = load_image(
                "pgu.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'r':
            self.image = load_image(
                "pgr.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'd':
            self.image = load_image(
                "pgd.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))

    def update(self, time, target):
        if self.mode == 3:
            self.ghost_run_animation()
        elif self.mode == 4:
            self.ghost_eyes_animation()
        else:
            self.pink_ghost_animation()
        super().update(time, target)


class Ghost3(AbstractGhost):
    def __init__(self, screen, *group, coords, pacman):
        super().__init__(screen, *group, coords=coords, pacman=pacman)
        self.image = load_image(
            "bgr.png", -1)
        self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.update_coords()
        self.speed *= 0.7
        self.respawntime = 25000

    def blue_ghost_animation(self):
        if self.napr == 'l':
            self.image = load_image(
                "bgl.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'u':
            self.image = load_image(
                "bgu.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'r':
            self.image = load_image(
                "bgr.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'd':
            self.image = load_image(
                "bgd.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))

    def update(self, time, target):
        if self.mode == 3:
            self.ghost_run_animation()
        elif self.mode == 4:
            self.ghost_eyes_animation()
        else:
            self.blue_ghost_animation()
        super().update(time, target)


class Ghost4(AbstractGhost):
    def __init__(self, screen, *group, coords, pacman):
        super().__init__(screen, *group, coords=coords, pacman=pacman)
        self.image = load_image(
            "ogr.png", -1)
        self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        self.update_coords()
        self.speed *= 1
        self.respawntime = 40000

    def orange_ghost_animation(self):
        if self.napr == 'l':
            self.image = load_image(
                "ogl.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'u':
            self.image = load_image(
                "ogu.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'r':
            self.image = load_image(
                "ogr.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))
        if self.napr == 'd':
            self.image = load_image(
                "ogd.png", -1)
            self.image = pygame.transform.scale(self.image, (self.board.cell_size, self.board.cell_size))

    def update(self, time, target):
        if self.mode == 3:
            self.ghost_run_animation()
        elif self.mode == 4:
            self.ghost_eyes_animation()
        else:
            self.orange_ghost_animation()
        super().update(time, target)


class Pacman(AbstractMob):  # пакман
    def __init__(self, screen, *group, coords):
        super().__init__(screen, *group, coords=coords)
        self.update_coords()
        self.napr = 'r'

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

        elif (self.napr == 'd' and not
        self.board.get_cell(
            (self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height + self.speed // tick))[2]):
            self.y += self.speed / tick

        self.stabilize()
        self.update_coords()
        self.board.getitem((self.x + self.rect.width // 2, self.y + self.rect.height // 2))
        self.updateanimation(time)
