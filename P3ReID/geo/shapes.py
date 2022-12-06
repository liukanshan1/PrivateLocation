import math
import random
import matplotlib.pyplot as plt
import numpy as np

from geo.location import encLocation


class Area:
    """一个平面"""

    def __init__(self, p1, p2, p3):
        self.A = (p2.y - p1.y) * (p3.z - p1.z) - (p2.z - p1.z) * (p3.y - p1.y)
        self.B = (p2.z - p1.z) * (p3.x - p1.x) - (p2.x - p1.x) * (p3.z - p1.z)
        self.C = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
        self.D = -self.A * p1.x - self.B * p1.y - self.C * p1.z

    def is_inside(self, point):
        return self.A * point.x + self.B * point.y + self.C * point.z + self.D == 0

    def get_x(self, y, z):
        if self.A == 0:
            return 0
        return -(self.B * y + self.C * z + self.D) / self.A

    def get_y(self, x, z):
        if self.B == 0:
            return 0
        return -(self.A * x + self.C * z + self.D) / self.B

    def get_z(self, x, y):
        if self.C == 0:
            return 0
        return -(self.A * x + self.B * y + self.D) / self.C

    def __str__(self):
        return "A: " + str(self.A) + " B: " + str(self.B) + " C: " + str(self.C) + " D: " + str(self.D)


class Point:
    """一个点"""

    def __init__(self, loc):
        if loc is None:
            self.x, self.y, self.z = 0, 0, 0
        else:
            self.x, self.y, self.z = loc.toXYZ()

    @staticmethod
    def create_point(x, y, z):
        point = Point(None)
        point.x, point.y, point.z = x, y, z
        return point

    def get_distant(self, point):
        return math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2)

    @staticmethod
    def distant(point1, point2):
        return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2)

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y) + " z: " + str(self.z)


class Triangle:
    """三角形"""

    def __init__(self, loc1, loc2, loc3):
        if loc1 is None:
            self.point1 = None
            self.point2 = None
            self.point3 = None
            self.max_x = None
            self.min_x = None
            self.max_y = None
            self.min_y = None
            self.max_z = None
            self.min_z = None
            self.area = None
            self.a = None
            self.b = None
            self.c = None
            self.square = None
        else:
            self.point1 = Point(loc1)
            self.point2 = Point(loc2)
            self.point3 = Point(loc3)
            self.max_x = max(self.point1.x, self.point2.x, self.point3.x)
            self.min_x = min(self.point1.x, self.point2.x, self.point3.x)
            self.max_y = max(self.point1.y, self.point2.y, self.point3.y)
            self.min_y = min(self.point1.y, self.point2.y, self.point3.y)
            self.max_z = max(self.point1.z, self.point2.z, self.point3.z)
            self.min_z = min(self.point1.z, self.point2.z, self.point3.z)
            self.area = Area(self.point1, self.point2, self.point3)
            self.a = Point.distant(self.point1, self.point2)
            self.b = Point.distant(self.point2, self.point3)
            self.c = Point.distant(self.point3, self.point1)
            p = (self.a + self.b + self.c) / 2
            self.square = math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    @staticmethod
    def create_triangle(p1, p2, p3):
        t = Triangle(None, None, None)
        t.point1 = p1
        t.point2 = p2
        t.point3 = p3
        t.max_x = max(t.point1.x, t.point2.x, t.point3.x)
        t.min_x = min(t.point1.x, t.point2.x, t.point3.x)
        t.max_y = max(t.point1.y, t.point2.y, t.point3.y)
        t.min_y = min(t.point1.y, t.point2.y, t.point3.y)
        t.max_z = max(t.point1.z, t.point2.z, t.point3.z)
        t.min_z = min(t.point1.z, t.point2.z, t.point3.z)
        t.area = Area(t.point1, t.point2, t.point3)
        t.a = Point.distant(t.point1, t.point2)
        t.b = Point.distant(t.point2, t.point3)
        t.c = Point.distant(t.point3, t.point1)
        p = (t.a + t.b + t.c) / 2
        t.square = math.sqrt(p * (p - t.a) * (p - t.b) * (p - t.c))
        return t

    def get_square(self):
        return self.square

    def is_inside(self, point):
        if point.x > self.max_x or point.x < self.min_x:
            return False
        if point.y > self.max_y or point.y < self.min_y:
            return False
        if point.z > self.max_z or point.z < self.min_z:
            return False
        if not self.area.is_inside(point):
            return False
        triangle1 = Triangle.create_triangle(self.point1, self.point2, point)
        triangle2 = Triangle.create_triangle(self.point2, self.point3, point)
        triangle3 = Triangle.create_triangle(self.point3, self.point1, point)
        if not self.square == triangle1.get_square() + triangle2.get_square() + triangle3.get_square():
            return False
        # 允许一些误差值
        # if not abs(self.square - (triangle1.get_square() + triangle2.get_square() + triangle3.get_square())) < 0.1:
        #     return False
        return True

    def get_point(self):
        # 一定概率上关注三个角
        # coin = random.choice([0, 0, 0, 0, 1, 2, 3])
        # if coin == 0:
        #     while True:
        #         x = random.uniform(self.min_x, self.max_x)
        #         y = random.uniform(self.min_y, self.max_y)
        #         z = self.area.get_z(x, y)
        #         point = Point.create_point(x, y, z)
        #         if self.is_inside(point):
        #             return point
        # else:
        #     x_range = (self.max_x - self.min_x) * 0.25
        #     y_range = (self.max_y - self.min_y) * 0.25
        #     while True:
        #         if coin == 1:
        #             x = random.uniform(-x_range, x_range) + self.point1.x
        #             y = random.uniform(-y_range, y_range) + self.point1.y
        #         elif coin == 2:
        #             x = random.uniform(-x_range, x_range) + self.point2.x
        #             y = random.uniform(-y_range, y_range) + self.point2.y
        #         else:
        #             x = random.uniform(-x_range, x_range) + self.point3.x
        #             y = random.uniform(-y_range, y_range) + self.point3.y
        #         z = self.area.get_z(x, y)
        #         point = Point.create_point(x, y, z)
        #         if self.is_inside(point):
        #             return point
        while True:
            x = random.uniform(self.min_x, self.max_x)
            y = random.uniform(self.min_y, self.max_y)
            z = self.area.get_z(x, y)
            point = Point.create_point(x, y, z)
            if self.is_inside(point):
                return point

    def get_radius(self, point):
        triangle1 = Triangle.create_triangle(self.point1, self.point2, point)
        triangle2 = Triangle.create_triangle(self.point2, self.point3, point)
        triangle3 = Triangle.create_triangle(self.point3, self.point1, point)
        h1 = 2 * triangle1.get_square() / self.a
        h2 = 2 * triangle2.get_square() / self.b
        h3 = 2 * triangle3.get_square() / self.c
        return min(h1, h2, h3)

    def get_circles(self, num, strict=0.2):
        result = []
        for i in range(num):
            while True:
                point = self.get_point()
                radius = self.get_radius(point)
                if Triangle.filter(result, [point, radius], strict):
                    break
            result.append([point, radius])
        return result

    @staticmethod
    def filter(circles, circle, strict=0.2):
        # TODO：使用人工智能
        for round in circles:
            distant = Point.distant(round[0], circle[0])
            # 不允许重叠
            # if distant <= abs(round[1] - circle[1]):
            #     return False
            # 不允许相交
            # if distant < round[1] + circle[1]:
            #     return False
            # 允许一定程度相交
            if distant < (round[1] + circle[1]) * strict + abs(round[1] - circle[1]) * (1-strict):
                return False
        return True

    def encrypt(self, pk, num=150):
        circles = self.get_circles(num)
        result = []
        for circle in circles:
            enc_loc = encLocation(pk, [], circle[0].x, circle[0].y, circle[0].z, circle[1], True)
            result.append(enc_loc)
        return result

    def check(self, circles, num=10000):
        inside = 0
        for i in range(num):
            dot = self.get_point()
            for circle in circles:
                if Point.distant(circle[0], dot) <= circle[1]:
                    inside += 1
                    break
        return inside/num


class Rectangle:
    """长方形"""

    def __init__(self, loc1, loc2, loc3, loc4):
        if loc1 is None:
            self.point1 = None
            self.point2 = None
            self.point3 = None
            self.point4 = None
        else:
            self.point1 = Point(loc1)
            self.point2 = Point(loc2)
            self.point3 = Point(loc3)
            self.point4 = Point(loc4)
            self.triangle1 = Triangle.create_triangle(self.point1, self.point2, self.point3)
            self.triangle2 = Triangle.create_triangle(self.point3, self.point4, self.point1)
            self.triangle3 = Triangle.create_triangle(self.point1, self.point2, self.point4)
            self.triangle4 = Triangle.create_triangle(self.point2, self.point3, self.point4)

    @staticmethod
    def create_rectangle(p1, p2, p3, p4):
        r = Rectangle(None, None, None, None)
        r.point1 = p1
        r.point2 = p2
        r.point3 = p3
        r.point4 = p4
        r.triangle1 = Triangle.create_triangle(r.point1, r.point2, r.point3)
        r.triangle2 = Triangle.create_triangle(r.point3, r.point4, r.point1)
        r.triangle3 = Triangle.create_triangle(r.point1, r.point2, r.point4)
        r.triangle4 = Triangle.create_triangle(r.point2, r.point3, r.point4)
        return r

    def get_circles(self, num, strict=0.3):
        num = round(num / 4)
        result = []
        result.extend(self.triangle1.get_circles(num, strict))
        result.extend(self.triangle2.get_circles(num, strict))
        result.extend(self.triangle3.get_circles(num, strict))
        result.extend(self.triangle4.get_circles(num, strict))
        return result

    def encrypt(self, pk, num=200):
        circles = self.get_circles(num)
        result = []
        for circle in circles:
            enc_loc = encLocation(pk, [], circle[0].x, circle[0].y, circle[0].z, circle[1], True)
            result.append(enc_loc)
        return result


def plot_circle(center=(3, 3), r=2):
    x = np.linspace(center[0] - r, center[0] + r, 5000)
    y1 = np.sqrt(r ** 2 - (x - center[0]) ** 2) + center[1]
    y2 = -np.sqrt(r ** 2 - (x - center[0]) ** 2) + center[1]
    plt.plot(x, y1, c='k')
    plt.plot(x, y2, c='k')


if __name__ == '__main__':
    # p1 = Point.create_point(0, 0, 0)
    # p2 = Point.create_point(400, 0, 0)
    # p3 = Point.create_point(400, 300, 0)
    # p4 = Point.create_point(0, 300, 0)
    # rec = Rectangle.create_rectangle(p1, p2, p3, p4)
    # circles = rec.get_circles(150)
    # fig = plt.figure(num=1, figsize=(4, 4))
    # plt.xlim(-5, 405)
    # plt.ylim(-5, 405)
    # # plt.plot([400, 0], [0, 0])
    # # plt.plot([400, 400], [0, 300])
    # # plt.plot([400, 0], [300, 300])
    # # plt.plot([0, 0], [300, 0])
    # for circle in circles:
    #     plot_circle(center=(circle[0].x, circle[0].y), r=circle[1])
    # plt.show()

    # p1 = Point.create_point(400, 200, 0)
    # p2 = Point.create_point(0, 400, 0)
    # p3 = Point.create_point(0, 0, 0)
    # triangle = Triangle.create_triangle(p1, p2, p3)
    # fig = plt.figure(num=1, figsize=(4, 4))
    # plt.xlim(-5, 405)
    # plt.ylim(-5, 405)
    # # plt.plot([400, 0], [200, 400])
    # # plt.plot([400, 0], [200, 0])
    # # plt.plot([0, 0], [400, 0])
    # circles = triangle.get_circles(100)
    # for circle in circles:
    #     plot_circle(center=(circle[0].x, circle[0].y), r=circle[1])
    # plt.show()

    p1 = Point.create_point(400, 200, 0)
    p2 = Point.create_point(0, 400, 0)
    p3 = Point.create_point(0, 0, 0)
    triangle = Triangle.create_triangle(p1, p2, p3)
    res = []
    for i in range(1000):
        circles = triangle.get_circles(100)
        res.append(triangle.check(circles))
    print(min(res))

