from enum import Enum
import random

from constants import *


def case_red():
    '''
    Ak je červený
    :return:
    '''
    # X < +500 a Y < +500
    return random.randint(-SIZE, int(SIZE / 10)), random.randint(-SIZE, int(SIZE / 10))


def case_green():
    '''
    Ak je zelený
    :return:
    '''
    # X > -500 a Y < +500
    return random.randint(-int(SIZE / 10), SIZE), random.randint(-SIZE, int(SIZE / 10))


def case_blue():
    '''
    Ak je modrý
    :return:
    '''
    # X < +500 a Y > -500
    return random.randint(-SIZE, int(SIZE / 10)), random.randint(-int(SIZE / 10), SIZE)


def case_purple():
    '''
    Ak je fialový
    :return:
    '''
    # X > -500 a Y > -500
    return random.randint(-int(SIZE / 10), SIZE), random.randint(-int(SIZE / 10), SIZE)


class Point:
    class Color(Enum):
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        PURPLE = (255, 0, 255)

    def __init__(self, color: Color):
        self.pos: tuple[int, int] = self.determine_position(color)  # priradenie pozície podľa farby
        # Atribúty farieb pre kazde k hodnoty
        self.color = color

        self.k1_color = self.color
        self.k3_color = self.color
        self.k7_color = self.color
        self.k15_color = self.color

    def hard_set_position(self, x, y):
        '''
        Natvrdo priradí pozíciu bodu
        :param x:
        :param y:
        :return:
        '''
        self.pos = (x, y)

    def determine_position(self, color: Color) -> tuple[int, int]:
        '''
        Vráti pozíciu nového bodu
        :param color:
        :return:
        '''
        if random.random() < 0.01:  # 1% šanca pre náhodnu pozíciu na celej ploche
            return random.randint(-SIZE, SIZE), random.randint(-SIZE, SIZE)

        switch = {  # switch pre priradenie pozície podľa farby
            Point.Color.RED: case_red,
            Point.Color.GREEN: case_green,
            Point.Color.BLUE: case_blue,
            Point.Color.PURPLE: case_purple
        }
        control = switch.get(color, lambda: "Invalid case")()
        return control
