from random import randint
from colors import COLORS


global chislo_ochkov, finished
chislo_ochkov = 0
finished = False
balls = []
polygons = []
v = []
v2 = []
a2 = []
g = 0
h = 0


"Функция создания параметров нового шара"
def new_ball():
    x = randint(100, 700)
    y = randint(100, 500)
    r = randint(30, 50)
    color = COLORS[randint(0, 5)]
    balls.append([color, x, y, r])

"Функция присваивания скорости новому шару"
def ball_speed():
    vx = randint(-10, 10)
    vy = randint(-10, 10)
    v.append([vx, vy])

"Функция создания параметров нового квадрата"
def new_polygon():
    x2 = randint(100, 700)
    y2 = randint(100, 500)
    r2 = randint(50, 80)
    width = randint(3, 10)
    color2 = COLORS[randint(0, 5)]
    polygons. append([color2, x2, y2, r2, width])

"Функция присваивания скорости новому квадрату"
def polygon_speed():
    vx2 = randint(-10, 10)
    vy2 = randint(-10, 10)
    v2.append([vx2, vy2])

"Функция присваивания ускорения новому квадрату"
def polygon_acceleration():
    ax2 = randint(-1, 1)
    ay2 = randint(-1, 1)
    a2.append([ax2, ay2])

"Функция проверки попадания игрока по квадрату"
def proverka_najatia2(coordinaty_najatiya, coordinata_kvadrata_x, coordinata_kvadrata_y, shirina_kvadrata):
    global najal2
    najal2 = False
    coordinata_najatiya_x = coordinaty_najatiya[0]
    coordinata_najatiya_y = coordinaty_najatiya[1]

    # проверка попадания в квадрат
    raznost1 = (coordinata_najatiya_x - coordinata_kvadrata_x)
    raznost2  = (coordinata_najatiya_y - coordinata_kvadrata_y)
    if raznost1 > 0 and raznost2 > 0 and raznost1 < shirina_kvadrata and raznost2 < shirina_kvadrata:
        najal2 = True

"Функция проверки попадания игрока по шару"
def proverka_najatia(coordinaty_najatiya, coordinata_kruga_x, coordinata_kruga_y, radius_kruga):
    global najal
    najal = False
    coordinata_najatiya_x = coordinaty_najatiya[0]
    coordinata_najatiya_y = coordinaty_najatiya[1]

    # проверка попадания в шарик по теореме Пифагора
    cvadrat_rasstoiania = (coordinata_kruga_x - coordinata_najatiya_x) ** 2 + (
                coordinata_kruga_y - coordinata_najatiya_y) ** 2
    if cvadrat_rasstoiania < radius_kruga ** 2:
        najal = True


def nachalo_igry():
    "Создаём изначально несколько шаров  и квадратов"
    for i in range(5, 10):
        new_ball()
    for i in range(len(balls)):
        ball_speed()
    for i in range(5, 10):
        new_polygon()
    for i in range(len(polygons)):
        polygon_speed()
        polygon_acceleration()

def tick(chislo_ochkov):
    #Здесь собраны все события, происходящие независимо от действий игрока с течением времени

    # Если ничего не делать, число очков постепенно уменьшается
    chislo_ochkov -= 1

    "Изменение положения шаров и квадратов"
    for i in range(len(balls)):
        balls[i][1] += v[i][0]
        balls[i][2] += v[i][1]
    for i in range(len(polygons)):
        v2[i][0] += a2[i][0]
        v2[i][1] += a2[i][1]
        polygons[i][1] += v2[i][0]
        polygons[i][2] += v2[i][1]

        "Отражение шаров от стенок"
    for i in range(len(balls)):
        if balls[i][1] - 2 * balls[i][3] < 0 and v[i][0] < 0 or balls[i][1] + 2 * balls[i][3] > 1200 and v[i][0] > 0:
            k = randint(5, 18)
            v[i][0] = -k * v[i][0] / 10
            "Ограничим скорость шариков"
            if v[i][0] < -30:
                v[i][0] = -5
            if v[i][0] > 30:
                v[i][0] = 5

        if balls[i][2] - 2 * balls[i][3] < 0 and v[i][1] < 0 or balls[i][2] + 2 * balls[i][3] > 1200 and v[i][1] > 0:
            t = randint(5, 18)
            v[i][1] = -t * v[i][1] / 10

            "Ограничим скорость шариков"
            if v[i][1] < -30:
                v[i][1] = 5
            if v[i][1] > 30:
                v[i][1] = -5

    "Отражение квадратов от стенок"
    for i in range(len(polygons)):
        if polygons[i][1] < 0 and v2[i][0] < 0 or polygons[i][1] + polygons[i][3] > 1200 and v2[i][0] > 0:
            k = randint(5, 18)
            v2[i][0] = -k * v[i][0] / 10
            a2[i][0] = randint(-1, 1)
            "Ограничим скорость квадратов"
            if v2[i][0] < -20:
                v2[i][0] = 5
            if v2[i][0] > 20:
                v2[i][0] = -5

        if polygons[i][2] < 0 and v2[i][1] < 0 or polygons[i][2] + polygons[i][3] > 1200 and v2[i][1] > 0:
            t = randint(5, 18)
            v2[i][1] = -t * v2[i][1] / 10
            a2[i][1] = randint(-1, 1)
            "Ограничим скорость квадратов"
            if v2[i][1] < -20:
                v2[i][1] = 5
            if v2[i][1] > 20:
                v2[i][1] = -5
    # И если шаров и квадратов слишком много - игра заканчивается
    if len(balls) + len(polygons) > 40:
        finished = True



def handler(eventbutton, eventpos, chislo_ochkov):
    #Здесь собрано всё связанное с обработкой событий от мыши
    g=0
    h=0
    if eventbutton == 1:

        for i in range(len(balls)):
            proverka_najatia(eventpos, balls[i][1], balls[i][2], balls[i][3])

            "Если попали по шару - удаляем его, делаем новый, счёт увеличивается"

            if najal is True:
                new_ball()
                # Заменяем старый шар на новый
                balls[i] = balls[len(balls) - 1]
                balls.pop(len(balls) - 1)
                # Заменяем скорость старого шара на скорость нового
                ball_speed()
                v[i] = v[len(v) - 1]
                v.pop(len(v) - 1)
                chislo_ochkov += 50
                g = 1

        for i in range(len(polygons)):
            proverka_najatia2(eventpos, polygons[i][1], polygons[i][2], polygons[i][3])

            "Если попали по квадрату - удаляем его, делаем новый, счёт увеличивается"

            if najal2 is True:
                new_polygon()
                # Заменяем старый квадрат на новый
                polygons[i] = polygons[len(polygons) - 1]
                polygons.pop(len(polygons) - 1)
                # Заменяем скорость старого квадрата на скорость нового
                polygon_speed()
                v2[i] = v2[len(v2) - 1]
                v2.pop(len(v2) - 1)
                # Заменяем ускорения старого квадрата на ускорение нового
                polygon_acceleration()
                a2[i] = a2[len(v2) - 1]
                a2.pop(len(a2) - 1)
                chislo_ochkov += 150
                h = 1
    # Если не попали - число шаров и квадратов увеличивается
    if g != 1:
        new_ball()
        ball_speed()

    if h != 1 and g != 1:
        new_polygon()
        polygon_speed()
        polygon_acceleration()


