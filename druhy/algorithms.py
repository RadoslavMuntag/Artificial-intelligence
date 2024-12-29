from point import Point
from constants import *

import heapq
import math
import random

IDE = 0


def get_distance(point1: Point, point2: Point):
    '''
    Vráti vzdialenosť medzi bodomi
    :param point1:
    :param point2:
    :return:
    '''
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(point1.pos, point2.pos)))




class KDTree:
    def __init__(self, point_list: list[Point], depth):
        '''
        Node v strome
        :param point_list:
        :param depth:
        '''
        point_list.sort(key=lambda point: point.pos[depth % 2])  # zoraď pody podľa dimenzie

        median_index = len(point_list) // 2  # index medianu

        self.current_point = point_list[median_index]  # bod priradený k node
        self.depth = depth  # hĺbka v strome

        # Rekurzívne priradenie listu vľavo
        self.left = None if median_index <= 0 else KDTree(list(point_list[:median_index]), depth + 1)

        # Rekurzívne priradenie listu vpravo
        self.right = None if median_index >= len(point_list) - 1 \
            else KDTree(list(point_list[median_index + 1:]), depth + 1)

    def insert_and_classify(self, point: Point, k: int):
        '''
        Vloženie bodu do stromu a klasifikovanie podľa k nearest neighbours
        :param point:
        :param k:
        :return:
        '''
        k_closest = self.insert_point(point, k)

        # Classify
        frequency = {}

        if K_Values[15]:
            for item in k_closest:  # histogram k15 farieb
                frequency[item[1].k15_color] = frequency.get(item[1].k15_color, 0) + 1

            new_color = max(frequency, key=frequency.get)  # vyber njčastejšiu farbu
            point.k15_color = new_color

        frequency = {}
        for i in range(8):  # vyhoď 8 najvzdialenejších
            heapq.heappop(k_closest)

        if K_Values[7]:
            for item in k_closest:  # histogram k7 farieb
                frequency[item[1].k7_color] = frequency.get(item[1].k7_color, 0) + 1

            new_color = max(frequency, key=frequency.get)  # vyber njčastejšiu farbu
            point.k7_color = new_color

        frequency = {}
        for i in range(4):  # vyhoď 4 najvzdialenejšie
            heapq.heappop(k_closest)

        if K_Values[3]:
            for item in k_closest:   # histogram k3 farieb
                frequency[item[1].k3_color] = frequency.get(item[1].k3_color, 0) + 1

            new_color = max(frequency, key=frequency.get) # vyber njčastejšiu farbu
            point.k3_color = new_color

        frequency = {}
        for i in range(2):  # vyhoď 4 najvzdialenejšie
            heapq.heappop(k_closest)

        if K_Values[1]:
            for item in k_closest:  # toto je absolútne zbytočné sú 4 ráno čo robím
                frequency[item[1].k1_color] = frequency.get(item[1].k1_color, 0) + 1

            new_color = max(frequency, key=frequency.get)
            point.k1_color = new_color


    def insert_point(self, point: Point, k: int):
        '''
        Rekurzívne priradí bod na leaf node, pri vynáraní nájde k najbližších bodov
        :param point:
        :param k:
        :return:
        '''
        dimension = self.depth % 2  # zisti dimenziu
        k_closest: list[tuple[float, Point]] = []  # max heap s najbližšími bodmi

        if point.pos[dimension] < self.current_point.pos[dimension]:  # dimenzia bodu je menšia choď vľavo
            if self.left is None:
                self.left = KDTree([point], self.depth + 1)  # vľavo je leaf, priraď nový node
            else:
                k_closest = self.left.insert_point(point, k)  # rekurzivne vľavo

            if self.classify_current(point, k_closest, k):  # pri vynáraní porovnaj node s novým bodom
                self.classify_right(point, k_closest, k)  # ak je dostatočne blízko po dimenzií choď do druhej vetvy
        else:
            if self.right is None:  # dimenzia bodu je väčšia choď vpravo
                self.right = KDTree([point], self.depth + 1)  # vpravo je leaf, priraď nový node
            else:
                k_closest = self.right.insert_point(point, k)  # rekurzivne vpravo

            if self.classify_current(point, k_closest, k):  # pri vynáraní porovnaj node s novým bodom
                self.classify_left(point, k_closest, k)  # ak je dostatočne blízko po dimenzií choď do druhej vetvy

        return k_closest

    def classify_current(self, point: Point, k_closest: list[tuple[float, Point]], k: int):
        '''
        Porovnanie aktuálneho node s Bodom
        :param point:
        :param k_closest:
        :param k:
        :return:
        '''
        dimension = self.depth % 2
        current_point: Point = self.current_point
        distance = get_distance(point, current_point)

        # v heape môže veľmi reálne byť bod s rovnakou vzdialenosťou a to pokazí heap,
        # pridaj veľmi malú hodnotu k vzdialenosti aby sa to nestalo
        distance += random.random() * 0.001

        if len(k_closest) < k:  # heap nie je plný, zaraď bod do heapu
            heapq.heappush(k_closest, (-distance, current_point))

        # Ak je aktuálny node bližšie k bodu ako bod na vrchu heapu, vymeň ich
        elif abs(current_point.pos[dimension] - point.pos[dimension]) < abs(k_closest[0][0]):
            if abs(distance) < abs(k_closest[0][0]):
                heapq.heappushpop(k_closest, (-distance, current_point))

        else:
            return False

        return True

    def classify_left(self, point: Point, k_closest: list[tuple[float, Point]], k: int):
        '''
        Rekurzívne prehľadaj ľavú vetvu
        :param point:
        :param k_closest:
        :param k:
        :return:
        '''
        if self.left is None:  # node je leaf, vráť sa
            return

        dimension = self.left.depth % 2
        current_point: Point = self.left.current_point
        distance = get_distance(point, current_point)
        distance += random.random() * 0.001  # znova ten istý problem so vzdialenosťou

        if len(k_closest) < k:  # heap nie je plný, zaraď bod do heapu
            heapq.heappush(k_closest, (-distance, current_point))

        # Ak je aktuálny node bližšie k bodu ako bod na vrchu heapu, vymeň ich
        elif abs(current_point.pos[dimension] - point.pos[dimension]) < abs(k_closest[0][0]): # porovnanie dimenzionalnej vzdialenosti
            if abs(distance) < abs(k_closest[0][0]):
                heapq.heappushpop(k_closest, (-distance, current_point))

        else:  # Dimenzinálna vzdialenosť je ďalej ako najväčšia vzdialenosť v heape, prezri len prilahlú stranu
            if current_point.pos[dimension] - point.pos[dimension] > 0:
                self.left.classify_left(point, k_closest, k)
            else:
                self.left.classify_right(point, k_closest, k)
            return

        self.left.classify_left(point, k_closest, k)  # rekurzívne vľavo
        self.left.classify_right(point, k_closest, k)  # rekurzívne vpravo

        return

    def classify_right(self, point: Point, k_closest: list[tuple[float, Point]], k: int):
        '''
        Rekurzívne prehľadávaj pravú vetvu
        :param point:
        :param k_closest:
        :param k:
        :return:
        '''

        # Úplne to isté ako pre ľavú vetvu, áno mohlo to byť krajšie, rekurzia je ťažká a aspoň to nerobil chat

        if self.right is None:
            return

        dimension = self.right.depth % 2
        current_point: Point = self.right.current_point
        distance = get_distance(point, current_point)
        distance += random.random() * 0.001

        if len(k_closest) < k:
            heapq.heappush(k_closest, (-distance, current_point))

        elif abs(current_point.pos[dimension] - point.pos[dimension]) < abs(k_closest[0][0]):
            if abs(distance) < abs(k_closest[0][0]):
                heapq.heappushpop(k_closest, (-distance, current_point))

        else:
            if current_point.pos[dimension] - point.pos[dimension] > 0:
                self.right.classify_left(point, k_closest, k)
            else:
                self.right.classify_right(point, k_closest, k)
            return

        self.right.classify_left(point, k_closest, k)
        self.right.classify_right(point, k_closest, k)

        return

    def debug_print(self):
        if self.left is not None:
            self.left.debug_print()

        if self.right is not None:
            self.right.debug_print()

        print(self.depth, self.current_point.pos, self.current_point.color)


def classify(new_point: Point, k, point_list: list[Point]):  # DEPRECATED, DON'T USE!!
    global IDE
    k_closest = []
    IDE += 1
    for current_point in point_list:
        distance = get_distance(new_point, current_point)
        distance += random.random() * 0.001

        if len(k_closest) < k:
            heapq.heappush(k_closest, (-distance, current_point.k15_color))

        elif -distance > k_closest[0][0]:
            heapq.heappushpop(k_closest, (-distance, current_point.k15_color))

    frequency = {}

    for item in k_closest:
        frequency[item[1]] = frequency.get(item[1], 0) + 1

    new_color = max(frequency, key=frequency.get)

    new_point.k15_color = new_color
    point_list.append(new_point)
