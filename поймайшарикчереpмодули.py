import pygame
from pygame.draw import *

import model
import colors

model.init()

def nachalo_igry():
    "Создаём изначально несколько шаров  и квадратов"
    for i in range(5, 10):
        model.new_ball()
    for i in range(len(model.balls)):
        model.ball_speed()
    for i in range(5, 10):
        model.new_polygon()
    for i in range(len(model.polygons)):
        model.polygon_speed()
        model.polygon_acceleration()

"Функция отрисовки нового квадрата"
def draw_polygon(color, x2, y2, r2, width):
    polygon(screen, color, [(x2, y2), (x2 + r2, y2), (x2 + r2, y2 + r2), (x2, y2 + r2)], width)

"Функция отрисовки нового шара"
def draw_ball(color, x, y, r):
    circle(screen, color, (x, y), r)

#Функция вывода счёта
def schet(chislo_ochkov):
    schetchik = pygame.font.Font(None, 100)
    textsurface = schetchik.render(str(chislo_ochkov), False, colors.RED)
    screen.blit(textsurface, (100, 100))

def zavershenie_igry(chislo_ochkov):
    clock.tick(FPS)
    cenok = pygame.font.Font(None, 200)

    textsurface = cenok.render('Game Over', False, colors.RED)
    screen.blit(textsurface, (200, 300))
    cenok2 = pygame.font.Font(None, 200)

    textsurface2 = cenok2.render('Ваши очки:', False, colors.GREEN)
    screen.blit(textsurface2, (200, 450))
    cenok3 = pygame.font.Font(None, 200)

    textsurface3 = cenok3.render(str(chislo_ochkov), False, colors.BLUE)
    screen.blit(textsurface3, (500, 600))
    pygame.display.update()


pygame.init()

nachalo_igry()

finished = False

FPS = 30
screen = pygame.display.set_mode((1200, 900))


clock = pygame.time.Clock()
pygame.display.update()

while not finished:
    clock.tick(FPS)
    global chislo_ochkov
    chislo_ochkov = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Обработка событий от мыши
            model.handler(event.button, event.pos, chislo_ochkov)

    #вызов обсчёта модели
    model.tick(chislo_ochkov)

    # И если шаров и квадратов слишком много - игра заканчивается
    if len(model.balls) + len(model.polygons) > 40:
        finished = True

    screen.fill(colors.BLACK)


    # Функция вывода счёта
    schet(chislo_ochkov)

    # Рисуем шары и квадраты
    for i in range(len(model.balls)):
        color, x, y, r = model.balls[i]
        draw_ball(color, x, y, r)

    for i in range(len(model.polygons)):
        color, x2, y2, r2, width = model.polygons[i]
        draw_polygon(color, x2, y2, r2, width)

    pygame.display.update()

screen.fill(colors.BLACK)

for i in range(100):
    zavershenie_igry(chislo_ochkov)

pygame.quit()