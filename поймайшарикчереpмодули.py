import pygame
from pygame.draw import *

import model
import colors

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
def schet():
    schetchik = pygame.font.Font(None, 100)
    textsurface = schetchik.render(str(model.chislo_ochkov), False, colors.RED)
    screen.blit(textsurface, (100, 100))

def zavershenie_igry():
    clock.tick(FPS)
    cenok = pygame.font.Font(None, 200)

    textsurface = cenok.render('Game Over', False, colors.RED)
    screen.blit(textsurface, (200, 300))
    cenok2 = pygame.font.Font(None, 200)

    textsurface2 = cenok2.render('Ваши очки:', False, colors.GREEN)
    screen.blit(textsurface2, (200, 450))
    cenok3 = pygame.font.Font(None, 200)

    textsurface3 = cenok3.render(str(model.chislo_ochkov), False, colors.BLUE)
    screen.blit(textsurface3, (500, 600))
    pygame.display.update()


pygame.init()

nachalo_igry()
FPS = 30
screen = pygame.display.set_mode((1200, 900))


clock = pygame.time.Clock()
pygame.display.update()

while not model.finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            model.finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Обработка событий от мыши
            model.handler(event.button, event.pos, model.chislo_ochkov)

    #вызов обсчёта модели
    model.tick(model.chislo_ochkov)

    screen.fill(colors.BLACK)


    # Функция вывода счёта
    schet()

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
    zavershenie_igry()

pygame.quit()