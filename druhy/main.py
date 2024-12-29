import random

import time
from point import Point
from algorithms import KDTree
from visualisation import Visualization
from constants import *


def init_points(point_list: list[Point]):
    '''
    Generovanie prvých 20 bodov
    :param point_list:
    :return:
    '''
    positions = [(4500, 4400), (4100, 3000), (1800, 2400), (2500, 3400), (2000, 1400)]
    for count, color in enumerate(Point.Color):
        for i in range(5):
            if count == 0:
                point = Point(color)
                point.hard_set_position(-positions[i][0], -positions[i][1])

            elif count == 1:
                point = Point(color)
                point.hard_set_position(positions[i][0], -positions[i][1])

            elif count == 2:
                point = Point(color)
                point.hard_set_position(-positions[i][0], positions[i][1])

            elif count == 3:
                point = Point(color)
                point.hard_set_position(positions[i][0], positions[i][1])

            point_list.append(point)


if __name__ == '__main__':
    TIMER = time.time()
    if GENERATE_BY_SEED:
        random.seed(SEED)

    point_list = []  # udržiava inštancie bodov pre vykreslenie
    init_points(point_list)

    root = KDTree(point_list, 0)  # root KD-tree

    for i in range(POINTS_TO_GENERATE):
        for color in Point.Color:  # Generovanie bodov pre každú farbu
            new_point = Point(color)  # Vygenerovanie nového bodu
            root.insert_and_classify(new_point, K)  # vloženie bodu KD-TREE a klasifikovanie bodu
            point_list.append(new_point)

    filename = 'data_K-NN_only.txt'
    with open(filename, 'a') as file:  # analýza času
        current_time = time.time() - TIMER
        file.write(f"{current_time} {POINTS_TO_GENERATE}\n")

    visual = Visualization(root, point_list)
    visual.start_simulation(TIMER)
