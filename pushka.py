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


class Rect:
    """
    Конструктор класса Rect
    Args:
    x, y, a, b - координаты верхнего левого угла и длины сторон
    vx, vy - скорости по осям
    color - цвет прямоугольника
    """
    def __init__(self, screen, x, y, a, b, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.a = a
        self.b = b
        self.color = color
        self.screen = screen
    def move(self):
        """Переместить прямоугольник по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        if self.x <= 0:
            self.vx = -self.vx/1.1
            self.vy = self.vy/1.1
            self.x += 10
        if self.x + self.a >= 800:
            self.vx = -self.vx / 1.1
            self.vy = self.vy / 1.1
            self.x -= 10
        if self.y <= 0:
            self.vy = -self.vy / 1.1
            self.vx = self.vx / 1.1
            self.y += 10
        if self.y + self.b >= 600:
            self.vy = -self.vy / 1.1
            self.vx = self.vx / 1.1
            self.y -= 10

    def draw(self):
        """
        Метод рисует прямоугольник
        """
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.a, self.b))

    def hittest(self, obj):
        """
        Метод проверяет координаты объеекта obj и если они попадают в область прямоугольника функция
        возвращает True
        """
        if obj.x > self.x and obj.x < self.x + self.a and obj.y > self.y and obj.y < self.y + self.b:
            return True


class Gun:
    """Конструктор класса Gun
    Args:
    x2, y2 - точки фиксированного конца пушки
    length - длина пушки
    width - ширина
    an - угол, задающий поворот от гоизонтального положения
    """
    def __init__(self, screen, x2, y2, x3, y3):
        self.screen = screen
        self.surface = surf
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREEN
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
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

    def draw1(self, x2, y2, x3, y3):
        """ Метод рисования пушки, в зависимости от положения мыши
        Args:
        x2, y2 - положения конца пушки
        """
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.an = math.atan2((-self.y3 + self.y2), (self.x3 - self.x2))
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


class Tank(Gun):
    """Конструктор класса Tank с параметрами:
    x, y - координаты танка
    vx - скорость по оси x
    """
    def __init__(self, screen, x, y, vx, vy, health, x2, y2, x3, y3):
        super().__init__(self, x, y, x3, y3)
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.health = health
        self.x3 = x3
        self.y3 = y3

    def draw(self):
        """
        Метод рисования танка
        """
        pygame.draw.rect(self.screen, BLACK, (self.x, self.y, 50, 20))
        pygame.draw.rect(self.screen, BLACK, (self.x+10, self.y-30, 30, 30))
        Tank.draw1(self, self.x + 25, self.y - 15, self.x3, self.y3)

    def move(self, d, p):
        """
        Метод перемещения с параметром, отвечающим за напраление
        """
        if d == 1:
            self.x += self.vx

        elif d == -1:
            self.x += -self.vx

        if p == 1:
            self.y -= self.vy

        elif p == -1:
            self.y += self.vy

    def hit(self, obj):
        """
        Метод, уменьшающий здоровье танка при попадании объекта
        """
        if obj.x > self.x and obj.x < self.x + 50 and obj.y<570 and obj.y > 520:
            self.health -= 10


screen = pygame.display.set_mode((WIDTH, HEIGHT))


def write(string, score, x, y, a):
    """
    Функция отрисовки текста с численным параметром score
    Args:
    x, y - положение левого верхнего угла поверхности с текстом
    score - численный параметр
    string - текстовая строка
    """
    f0 = pygame.font.Font(None, 50)
    if score > -1:
        text10 = f0.render(str(score), True, (a, 0, 0))
        screen.blit(text10, (x + 150, y))
    string = str(string)
    text20 = f0.render(string, True, (a, 0, 0))
    screen.blit(text20, (x, y))


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
Rects = []
for i in range(randint(5, 7)):
    x = randint(0, 600)
    y = randint(0, 400)
    a = randint(10, 30)
    b = randint(5, 20)
    vx = randint(-10, 10)
    vy = 0
    COLOR = GAME_COLORS[randint(0, 5)]
    my_rect = Rect(screen, x, y, a, b, vx, vy, COLOR)
    Rects.append(my_rect)
p = len(Rects)
bullet = 0
s = 0
score1 = score2 = 0
flag1 = flag2 = False
Bullets1 = []
Bullets2 = []
clock = pygame.time.Clock()
tank1 = Tank(screen, 300, 570, 20, 20, 100, 0, 0, 0, 0)
tank2 = Tank(screen, 500, 570, 20, 20, 100, 0, 0, 0, 0)
finished = False
fla = fld = flw = fls = False
fl_left = False
fl_right = True
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
control = 100
timer = 0

while not finished:
    control1 = control2 = 100
    s1 = len(Bullets1)
    s2 = len(Bullets2)
    screen.fill(WHITE)
    if tank1.health > 0:
        u, w = pygame.mouse.get_pos()
        tank1.x3 = u
        tank1.y3 = w
        Tank.draw(tank1)
    if tank2.health > 0:
        tank2.x3 = tank1.x
        tank2.y3 = tank1.y
        Tank.draw(tank2)
    l1 = len(Bombs)
    for i in range(l1):
        if Bombs[i].y > 565:
            Bombs.pop(i)
            j = randint(0, l-1)
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
        write('Нажмите 1 для активации 1 танка', -1, 100, 300, 180)
        write('WASD-движение 1', -1, 100, 340, 180)
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
            if event.key == pygame.K_a:
                fla = True
            elif event.key == pygame.K_w:
                flw = True
            elif event.key == pygame.K_s:
                fls = True
            elif event.key == pygame.K_d:
                fld = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                fla = False
            elif event.key == pygame.K_w:
                flw = False
            elif event.key == pygame.K_s:
                fls = False
            elif event.key == pygame.K_d:
                fld = False
            elif event.key == pygame.K_1:
                flag1 = True
            elif event.key == pygame.K_2:
                flag2 = True
        elif event.type == pygame.MOUSEMOTION:
            if flag2:
                Tank.targetting(tank2, event)
            if flag1:
                Tank.targetting(tank1, event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            Tank.fire2_start(tank2, event)
            Tank.fire2_start(tank1, event)
        elif event.type == pygame.MOUSEBUTTONUP:  # второй стреляет когда стреляет первый
            Tank.fire2_end(tank2, event)
            (x_mouse2, y_mouse2) = pygame.mouse.get_pos()
            angle2 = math.atan2((-tank1.y + 535), (tank1.x - tank2.x+30))
            new_ball2 = Bullet(screen, tank2.x+30, 535, 10, 120/2.5 * math.cos(angle2),  120/2.5 * math.sin(angle2), GAME_COLORS[randint(0, 5)], 10)
            Bullets2.append(new_ball2)
            Tank.fire2_end(tank1, event)
            (x_mouse1, y_mouse1) = pygame.mouse.get_pos()
            angle1 = math.atan2((-y_mouse1 + tank1.y-15), (x_mouse1 - tank1.x + 30))
            new_ball1 = Bullet(screen, tank1.x + 30, tank1.y-15, 10, POWER / 2.5 * math.cos(angle1),
                               POWER / 2.5 * math.sin(angle1), GAME_COLORS[randint(0, 5)], 10)
            Bullets1.append(new_ball1)
    if fl_right == True:
        Tank.move(tank2, 1, 0)
        if tank2.x > 700:
            fl_right = False
            fl_left = True
    elif fl_left == True:
        Tank.move(tank2, -1, 0)
        if tank2.x < 50:
            fl_right = True
            fl_left = False
    if fld == True:
            Tank.move(tank1, 1, 0)
    elif fla == True:
            Tank.move(tank1, -1, 0)
    if flw == True:
            Tank.move(tank1, 0, 1)
    elif fls == True:
            Tank.move(tank1, 0, -1)
    s1 = len(Bullets1)
    s2 = len(Bullets2)
    for i in range(p):
        Rect.move(Rects[i])
        Rect.draw(Rects[i])

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
        for j in range(i+1, l, 1):
            Target.collision(Targets[i], Targets[j], 2, 2)
    l1 = len(Bombs)
    for i in range(p):
        for j in range(s1):
            if Rect.hittest(Rects[i], Bullets1[j]) == True:
                Rects.pop(i)
                x = randint(0, 600)
                y = randint(0, 400)
                a = randint(10, 30)
                b = randint(5, 20)
                vx = randint(-10, 10)
                vy = 0
                COLOR = GAME_COLORS[randint(0, 5)]
                my_rect = Rect(screen, x, y, a, b, vx, vy, COLOR)
                Rects.append(my_rect)
    for i in range(p):
        for j in range(s2):
            if Rect.hittest(Rects[i], Bullets2[j]) == True:
                Rects.pop(i)
                x = randint(0, 600)
                y = randint(0, 400)
                a = randint(10, 30)
                b = randint(5, 20)
                vx = randint(-10, 10)
                vy = 0
                COLOR = GAME_COLORS[randint(0, 5)]
                my_rect = Rect(screen, x, y, a, b, vx, vy, COLOR)
                Rects.append(my_rect)
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
            if Bullets2[i].x > tank1.x and Bullets2[i].x < tank1.x + 50 and Bullets2[i].y < tank1.y+10 and Bullets2[i].y > tank1.y-30:
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
                if Bullets1[i].x > tank2.x and Bullets1[i].x < tank2.x + 50 and Bullets1[i].y < 570 and Bullets1[i].y > 520:
                    control1 = i
    if len(Bullets1) > 0:
        if control1 <= len(Bullets1):
            Bullets1.pop(control1)
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()