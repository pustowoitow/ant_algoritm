# -*- coding: utf8 -*-
# Алгоритм муравья
from math import sqrt
from random import random
import numpy as np
import numpy.random as rand

MAX_CITIES = 20
MAX_DISTANCE = 50
MAX_TIME = 150 * MAX_CITIES
INIT_PHEROMONE = 1.0 / MAX_CITIES

MAX_ANTS = MAX_CITIES * 25
ALPHA = 3  # вес фермента
BETA = 9  # коэффициент эвристики, влияние априорных знаний(1/d, где d - растояние)
RHO = .8  # Интенсивность. Коф. испарение равен 1 - RHO. По результатам тестов лучше использовать >= 0.5
QVAL = 100  # Кол. феромонов на один проход


class City(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ant(object):

    def __init__(self, start_city):
        self.cur_city = start_city
        self.path = [start_city]
        self.tour_length = 0.

    def move_to_city(self, city):
        global DISTANCE, MAX_CITIES
        self.path.append(city)
        self.tour_length += DISTANCE[self.cur_city][city]
        if len(self.path) == MAX_CITIES:
            self.tour_length += DISTANCE[self.path[-1]][self.path[0]]
        self.cur_city = city

    def can_move(self):
        global MAX_CITIES
        return len(self.path) < MAX_CITIES

    def reset(self, city):
        self.cur_city = city
        self.path = [city]
        self.tour_length = 0.


def get_random(l):
    r = random()
    cur_probability = 0
    cur_val = None

    for val, probability in l:
        cur_val = val
        cur_probability += probability
        if r <= cur_probability:
            break

    return cur_val


ANTS = []  # [MAX_ANTS]
DISTANCE = []  # [MAX_CITIES][MAX_CITIES]
PHEROMONE = []  # [MAX_CITIES][MAX_CITIES]
BEST = MAX_CITIES * MAX_DISTANCE
BEST_ANT = None


def init():
    global DISTANCE, PHEROMONE, ANTS

    MAX_TIME = 200 * MAX_CITIES
    INIT_PHEROMONE = 1.0 / MAX_CITIES

    MAX_ANTS = MAX_CITIES * MAX_CITIES

    for i in range(MAX_CITIES):
        PHEROMONE.append([INIT_PHEROMONE] * MAX_CITIES)

    # create ants
    to = 0
    for i in range(MAX_ANTS):
        ANTS.append(Ant(to))
        to += 1
        to = to % MAX_CITIES


def ant_product(from_city, to_city, ph=None):
    global DISTANCE, PHEROMONE, ALPHA, BETA
    ph = ph or PHEROMONE[from_city][to_city]
    return (ph ** ALPHA) * \
         ((1. / DISTANCE[from_city][to_city]) ** BETA)


def select_next_city(ant):
    global MAX_CITIES, PHEROMONE, DISTANCE
    denom = 0.
    not_visited = []

    for to in range(MAX_CITIES):
        if to not in ant.path:
            ap = ant_product(ant.cur_city, to)
            not_visited.append((to, ap))
            denom += ap

    assert not_visited
    not_visited = [(val, ap / denom) for (val, ap) in not_visited]
    to = get_random(not_visited)
    return to
    i = 0
    while True:
        to, ap = not_visited[i]
        p = ap / denom
        if random() < p:
            break
        i += 1
        i = i % len(not_visited)

    if False and len(not_visited) == MAX_CITIES - 1:
        for to_city, ap in not_visited:
            print ('%i %.03f %.01f %.02f' % (to_city, PHEROMONE[ant.cur_city][to_city], DISTANCE[ant.cur_city][to_city], ap / denom))
        print (to)
        raw_input()
    assert ant.cur_city != to
    return to


def simulate_ants():
    global ANTS, MAX_CITIES
    moving = 0

    for ant in ANTS:
        if ant.can_move():
            ant.move_to_city(select_next_city(ant))
            moving += 1

    return moving


def update_trails():
    global MAX_CITIES, PHEROMONE, RHO, INIT_PHEROMONE, ANTS

    # add new pheromone
    for ant in ANTS:
        pheromove_amount = QVAL / ant.tour_length

        for i in range(MAX_CITIES):
            if i == MAX_CITIES - 1:
                from_city = ant.path[i]
                to_city = ant.path[0]
            else:
                from_city = ant.path[i]
                to_city = ant.path[i + 1]
            assert from_city != to_city
            PHEROMONE[from_city][to_city] = PHEROMONE[from_city][to_city] * (1 - RHO) + pheromove_amount
            PHEROMONE[to_city][from_city] = PHEROMONE[from_city][to_city]


def restart_ants():
    global ANTS, BEST, BEST_ANT, MAX_CITIES
    to = 0

    for ant in ANTS:
        if ant.tour_length < BEST:
            BEST = ant.tour_length
            BEST_ANT = ant

        ant.reset(to)
        to += 1
        to = to % MAX_CITIES

if __name__ == '__main__':
    # print("Введите массив значений 20 на 20:")
    for i in range(0,MAX_CITIES):
        DISTANCE.append([int(j) for j in input().split()])
        if i==0:
            MAX_CITIES=len(DISTANCE[0])
        if i>=MAX_CITIES-1:
            break
    # print("Успешно! Данные получены!")
    # print("Полученный массив значений:")
    # print(DISTANCE)

# Генерация значений для тестирования
    # b=np.random.randint(1, 50, size=(20, 20))
    # i=range(0, 20)
    # for x in i:
    #     b[x][x]=0
    # print (b)
# Ввод значений массива
    init()
    cur_time = 0
    while cur_time < MAX_TIME:
        cur_time += 1
        # if cur_time % 100 == 0:
        #     print ('time:', cur_time, 'of', MAX_TIME)

        if simulate_ants() == 0:
            update_trails()
            cur_time != MAX_TIME and restart_ants()

#    print ("Наилучший путь:")
 #   print(BEST_ANT.path)
 #    print ("Расстояние для наилучшего пути:")
    print(int(BEST_ANT.tour_length))
