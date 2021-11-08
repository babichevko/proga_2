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


class Target(Ball):
    """ Класс, наследуемый от ball
    """
    def __init__(self, screen, x, y, r, vx, vy, color, g):
     super().__init__(screen, x, y, r, vx, vy, color, g)
     self.screen = screen

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
           obj: Обьект, с которым проверяется столкновение.
        Returns:
        Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (obj.x - self.x) ** 2 + (obj.y - self.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False

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

    def collision(self, obj, p, q):
        """ Метод столкновения целей между собой
        p - скорость по x объекта с которым сталкиваются
        q - скорость по y объекта с которым сталкиваются
        """
        if (self.x-obj.x)**2 + (self.y-obj.y)**2 <= (self.r + obj.r)**2:
            p = obj.vx
            q = obj.vy
            obj.vx = self.vx
            obj.vy = self.vy
            self.vx = p
            self.vy = q
            self.x -= (obj.x-self.x)/100

class Bullet(Ball):
    def __init__(self, screen, x, y, r, vx, vy, color, g):
     super().__init__(screen, x, y, r, vx, vy, color, g)
     self.screen = screen
    def draw(self):
        pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r
            )

    def delete(self, list):
        if list[i].vx and list[i].vy == 0:
            list.pop(i)


class Bomb(Ball):
    def __init__(self, screen, x, y, r, vx, vy, color, g):
     super().__init__(screen, x, y, r, vx, vy, color,g)
     self.screen = screen

    def draw(self):
        pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r
            )

    #def detonation(self, list):
        #if list[i].y > 570:
            #list.pop(i)


screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Tank(Gun):
    def __init__(self, screen, x, vx, health):
        super().__init__(self, x, y)
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = vx
        self.health = health

    def draw(self):
        pygame.draw.rect(self.screen, BLACK, (self.x, 550, 50, 20))
        pygame.draw.rect(self.screen, BLACK, (self.x+10, 520, 30, 30))
        Tank.draw1(self, self.x + 25, 535)

    def move(self, d):
        if d == 1:
            self.x += self.vx

        elif d == -1:
            self.x += -self.vx

    def hit(self, obj):
        if obj.x > self.x and obj.x < self.x + 50 and obj.y<570 and obj.y > 520:
            self.health -= 10


Targets = []
for i in range(randint(5, 7)):
    x = randint(0, 600)
    y = randint(0, 400)
    r = randint(20, 40)
    vx = randint(-10, 10)
    vy = 0
    COLOR = GAME_COLORS[randint(0, 5)]
    g = 0
    my_ball = Target(screen, x, y, r, vx, vy, COLOR, g)
    Targets.append(my_ball)
l = len(Targets)
bullet = 0
s = 0
score1 = score2 = 0
flag1 = flag2 = False
Bullets1 = []
Bullets2 = []
clock = pygame.time.Clock()
tank1 = Tank(screen, 300, 20, 100)
tank2 = Tank(screen, 500, 20, 100)
finished = False
fla = fld = False
fl_left = fl_right = False
Bombs = []
for i in range(l):
    x = Targets[i].x
    y = Targets[i].y
    r = 10
    vx = 0
    vy = 10
    g = 10
    new_bomb = Bomb(screen, x, y, r, vx, vy, BLACK, g)
    Bombs.append(new_bomb)
T = []
control = 100
for i in range(l):
    T.append(0)
timer = 0


def write(string, score, x, y, a):
    f0 = pygame.font.Font(None, 50)
    if score > -1:
        text10 = f0.render(str(score), True, (a, 0, 0))
        screen.blit(text10, (x + 150, y))
    string = str(string)
    text20 = f0.render(string, True, (a, 0, 0))
    screen.blit(text20, (x, y))


while not finished:
    control1 = control2 = 100
    if T[1] == 101:
        for i in range(l):
            T[i] = 0
    s1 = len(Bullets1)
    s2 = len(Bullets2)
    screen.fill(WHITE)
    if tank2.health > 0:
        Tank.draw(tank2)
    if tank1.health > 0:
        Tank.draw(tank1)
    l1 = len(Bombs)
    for i in range(l1):
        if Bombs[i].y > 565:
            Bombs.pop(i)
            j = randint(0, l - 1)
            x = Targets[j].x
            y = Targets[j].y
            r = 10
            vx = 0
            vy = 10
            g = 10
            new_bomb = Bomb(screen, x, y, r, vx, vy, BLACK, g)
            Bombs.append(new_bomb)
    for i in range(s1):
        Bullet.delete(Bullets1[i], Bullets1)
    write('score2:', score2, 610, 50, 180)
    write('score1:', score1, 10, 50, 180)
    if timer < 100:
        write('Нажмите 1 или 2 для выбора и переключения', -1, 100, 300, 180)
        write('AD-движение 1, стрелки - движение 2', -1, 100, 340, 180)
        timer += 1
    if tank2.health > 0:
        write('health2:', tank2.health, 610, 80, 180)
    else:
        write('health2:', 0, 610, 80, 180)
        write('Первый победил', -2, 300, 400, 180)
    if tank1.health > 0:
        write('health1:', tank1.health, 10, 80, 180)
    else:
        write('health1:', 0, 10, 80, 180)
        write('Второй победил', -2, 300, 400, 180)
    x1, y1 = pygame.mouse.get_pos()
    for i in range(l):
        Ball.draw(Targets[i])
        Ball.move(Targets[i])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                fl_left = True
            elif event.key == pygame.K_a:
                fla = True
            elif event.key == pygame.K_RIGHT:
                fl_right = True
            elif event.key == pygame.K_d:
                fld = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                fl_left = False
            if event.key == pygame.K_a:
                fla = False
            elif event.key == pygame.K_RIGHT:
                fl_right = False
            elif event.key == pygame.K_d:
                fld = False
            elif event.key == pygame.K_1:
                flag1 = True
                flag2 = False
            elif event.key == pygame.K_2:
                flag2 = True
                flag1 = False
        elif event.type == pygame.MOUSEMOTION:
            if flag2:
                Tank.targetting(tank2, event)
            if flag1:
                Tank.targetting(tank1, event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if flag2:
                Tank.fire2_start(tank2, event)
            if flag1:
                Tank.fire2_start(tank1, event)
        elif event.type == pygame.MOUSEBUTTONUP:
            if flag2:
                Tank.fire2_end(tank2, event)
                (x_mouse2, y_mouse2) = pygame.mouse.get_pos()
                angle2 = math.atan2((-y_mouse2 + 535), (x_mouse2 - tank2.x + 30))
                new_ball2 = Bullet(screen, tank2.x + 30, 535, 10, POWER / 2.5 * math.cos(angle2),
                                   POWER / 2.5 * math.sin(angle2), GAME_COLORS[randint(0, 5)], 10)
                Bullets2.append(new_ball2)
            elif flag1:
                Tank.fire2_end(tank1, event)
                (x_mouse1, y_mouse1) = pygame.mouse.get_pos()
                angle1 = math.atan2((-y_mouse1 + 535), (x_mouse1 - tank1.x + 30))
                new_ball1 = Bullet(screen, tank1.x + 30, 535, 10, POWER / 2.5 * math.cos(angle1),
                                   POWER / 2.5 * math.sin(angle1), GAME_COLORS[randint(0, 5)], 10)
                Bullets1.append(new_ball1)
    if flag2:
        if fl_right == True:
            Tank.move(tank2, 1)
        elif fl_left == True:
            Tank.move(tank2, -1)
    if flag1:
        if fld == True:
            Tank.move(tank1, 1)
        elif fla == True:
            Tank.move(tank1, -1)
    s1 = len(Bullets1)
    s2 = len(Bullets2)
    for i in range(s1):
        Bullet.draw(Bullets1[i])
        Bullet.move(Bullets1[i])
        for i in range(l):
            for j in range(s1):
                if Targets[i].hittest(Bullets1[j]) == True:
                    Targets.pop(i)
                    score1 += 1
                    x = randint(0, 600)
                    y = randint(0, 400)
                    r = randint(20, 40)
                    vx = randint(-10, 10)
                    vy = 0
                    COLOR = GAME_COLORS[randint(0, 5)]
                    g = 0
                    my_ball = Target(screen, x, y, r, vx, vy, COLOR, g)
                    Targets.append(my_ball)
    s1 = len(Bullets1)
    s2 = len(Bullets2)
    for i in range(s2):
        Bullet.draw(Bullets2[i])
        Bullet.move(Bullets2[i])
        for i in range(l):
            for j in range(s2):
                if Targets[i].hittest(Bullets2[j]) == True:
                    Targets.pop(i)
                    score2 += 1
                    x = randint(0, 600)
                    y = randint(0, 400)
                    r = randint(20, 40)
                    vx = randint(-10, 10)
                    vy = 0
                    COLOR = GAME_COLORS[randint(0, 5)]
                    g = 0
                    my_ball = Target(screen, x, y, r, vx, vy, COLOR, g)
                    Targets.append(my_ball)
    for i in range(l):
        for j in range(i + 1, l, 1):
            Target.collision(Targets[i], Targets[j], 2, 2)
    l1 = len(Bombs)
    for i in range(l1):
        Bombs[i].move()
        Bombs[i].draw()
        if flag1:
            Tank.hit(tank1, Bombs[i])
        if flag2:
            Tank.hit(tank2, Bombs[i])

    if flag2:
        Tank.power_up(tank2)
    if flag1:
        Tank.power_up(tank1)
    s1 = len(Bullets1)
    s2 = len(Bullets2)
    l1 = len(Bombs)
    if flag2:
        if l1 > 0:
            for i in range(l1):
                Tank.hit(tank2, Bombs[i])
    if flag1:
        if l1 > 0:
            for i in range(l1):
                Tank.hit(tank1, Bombs[i])
    if tank1.health > 0:
        if s2 > 0:
            for i in range(s2):
                Tank.hit(tank1, Bullets2[i])
                if Bullets2[i].x > tank1.x and Bullets2[i].x < tank1.x + 50 and Bullets2[i].y < 570 and Bullets2[
                    i].y > 520:
                    control2 = i
    if len(Bullets2) > 0:
        if control2 <= len(Bullets2):
            Bullets2.pop(control2)
    if tank2.health > 0:
        s1 = len(Bullets1)
        s2 = len(Bullets2)
        if s1 > 0:
            for i in range(s1):
                Tank.hit(tank2, Bullets1[i])
                if Bullets1[i].x > tank2.x and Bullets1[i].x < tank2.x + 50 and Bullets1[i].y < 570 and Bullets1[
                    i].y > 520:
                    control1 = i
    if len(Bullets1) > 0:
        if control1 <= len(Bullets1):
            Bullets1.pop(control1)
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()