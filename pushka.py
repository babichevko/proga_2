import math
from random import randint

import pygame
pygame.init()

FPS = 30

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
score = 0
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1000
HEIGHT = 800

surf = pygame.Surface((200, 100))


class Ball:
    def __init__(self, screen: pygame.Surface, x, y, r, vx, vy, color, g):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        r - радиус мяча
        vx, vy, g - скорости по x, y и ускорение по y
        color - цвет
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.g = g
        self.vy = vy
        self.color = color
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy += -self.g/30
        self.x += self.vx
        self.y -= self.vy
        if self.x - self.r <= 0:
            self.vx = -self.vx/1.1
            self.vy = self.vy/1.1
            self.x += 10
        if self.x + self.r >= 800:
            self.vx = -self.vx / 1.1
            self.vy = self.vy / 1.1
            self.x -= 10
        if self.y - self.r <= 0:
            self.vy = -self.vy / 1.1
            self.vx = self.vx / 1.1
            self.y += 10
        if self.y + self.r >= 600:
            self.vy = -self.vy / 1.1
            self.vx = self.vx / 1.1
            self.y -= 10
        if self.x <= 0 or self.x >= 800 or self.y <= 0 or self.y >= 600:
            self.vx = 0
            self.vy = 0
            self.g = 0

    def draw(self):
        """Нарисовать шарик
         Метод рисует шарик в координатах x, y
        """
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (obj.x-self.x)**2+(obj.y-self.y)**2 <= (self.r+obj.r)**2:
            return True
        else:
            return False

g = 10

class Gun:
    """Конструктор класса Gun
    Args:
    x2, y2 - точки фиксированного конца пушки
    length - длина пушки
    width - ширина
    an - угол, задающий поворот от гоизонтального положения
    """
    def __init__(self, screen, x2, y2):
        self.screen = screen
        self.surface = surf
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREEN
        self.x2 = x2
        self.y2 = y2
        self.length = 30
        self.width = 5

    def fire2_start(self, event):
        """ Задает начало выстрела, устанавливая параметр на значение 1
        """
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        (x_mouse, y_mouse) = pygame.mouse.get_pos()
        new_ball = Ball(self.screen, 100, 580, 20, 10, 10 * math.tan(self.an), RED, g)
        self.an = math.atan2((-y_mouse + self.y2), (x_mouse - self.x2))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        self.f2_on = 0
        self.f2_power = 10
        self.length = 30
        self.width = 5

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-400) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREEN

    def draw1(self, x2, y2):
        """ Метод рисования пушки, в зависимости от положения мыши
        Args:
        x2, y2 - положения конца пушки
        """
        (x_mouse, y_mouse) = pygame.mouse.get_pos()
        self.x2 = x2
        self.y2 = y2
        self.an = math.atan2((-y_mouse + self.y2), (x_mouse - self.x2))
        length_up = self.length + self.f2_power
        width_half = self.width / 2
        pygame.draw.polygon(self.screen, self.color,
                            ((self.x2 - width_half * math.sin(self.an),
                              self.y2 - width_half * math.cos(self.an)),
                             (self.x2 + width_half * math.sin(self.an),
                              self.y2 + width_half * math.cos(self.an)),
                             (self.x2 + width_half * math.sin(self.an) + length_up * math.cos(self.an),
                              self.y2 + width_half * math.cos(self.an) - length_up * math.sin(self.an)),
                             (self.x2 - width_half * math.sin(self.an) + length_up * math.cos(self.an),
                              self.y2 - width_half * math.cos(self.an) - length_up * math.sin(self.an))))

    def power_up(self):
        """Метод зарядки пушки
        """
        global POWER
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
                POWER = self.f2_power
            self.color = RED
        else:
            self.color = GREEN


class Target:
    def __init__(self, type=1):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(15, 50)
        self.vx = randint(-7, 7)
        self.vy = randint(-7, 7)
        self.color = GAME_COLORS[randint(0,5)]
        self.live=type
        self.type=type

    def hit(self, point=1):
        """Попадание шарика в цель."""
        self.live -= 1
        global points
        points += point

    def draw(self):
        if(self.type==1):
            pygame.draw.circle(
                screen,
                self.color,
                (self.x, self.y),
                self.r
            )
            pygame.draw.circle(
                screen,
                BLACK,
                (self.x, self.y),
                self.r,
                width=1
            )
        elif self.type == 2:
            pygame.draw.rect(
                screen,
                self.color,
                (self.x-self.r, self.y-self.r, self.r*2,self.r*2)
            )
            pygame.draw.rect(
                screen,
                BLACK,
                (self.x-self.r, self.y-self.r, self.r*2,self.r*2),
                width=1
            )

    def move(self):
        """перемещает себя значение скорости"""
        self.x += self.vx
        self.y += self.vy


def drawscore():
    """вывод очков на экран"""
    f1 = pygame.font.Font(None, 36)
    tbl = 'points: '
    tbl += str(points)
    text1 = f1.render(tbl, True, BLACK)
    screen.blit(text1, (10, 10))


def showtext():
    f1 = pygame.font.Font(None, 36)
    tbl = 'вы уничтожили цель за '
    tbl += str(bulletshow)
    tbl += ' выстрелов'
    text1 = f1.render(tbl, True, BLACK)
    screen.blit(text1, (180, 250))


def collision(obj):
    """функция коллизии, получает объект и при столкновении отражает его от стен
    Xbound, Ybound - границы экрана, заданы вне функции
    """
    if(obj.x + obj.r > WIDTH):
        obj.vx *= -1
        obj.x = WIDTH-obj.r
    elif(obj.x - obj.r < 0):
        obj.vx *= -1
        obj.x = obj.r
    elif(obj.y - obj.r < 0):
        obj.vy *= -1
        obj.y = obj.r
    elif(obj.y + obj.r > HEIGHT):
        obj.vy *= -1
        obj.y = HEIGHT-obj.r


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
bulletshow=0
balls = []
points = 0

clock = pygame.time.Clock()
gun = Gun(screen, 300, 20)
target1 = Target(1)
target2 = Target(2)
finished = False

do_showtext=0
pause = False

while not finished:
    screen.fill(WHITE)
    gun.draw1()
    target1.draw()
    target2.draw()
    for b in balls:
        b.draw()
    drawscore()
    pause=False
    if(do_showtext > 0):
        showtext()
        do_showtext-=1
        pause=True
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if(not pause):
                gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            if(not pause):
                gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target1):
            target1.hit()
            if(target1.live == 0):
                target1 = Target(1)
                bulletshow=bullet
                bullet = 0
                balls = []
                do_showtext=100
        if b.hittest(target2):
            target2.hit()
            if(target2.live == 0):
                target2 = Target(2)
                bulletshow=bullet
                bullet = 0
                balls = []
                do_showtext=100
    gun.power_up()
    target1.move()
    target2.move()
    collision(target1)
    collision(target2)
pygame.quit()