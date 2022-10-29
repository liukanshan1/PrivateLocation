import math
from random import random


class Area:
    def __init__(self, p1, p2, p3):
        self.A = (p2.y - p1.y) * (p3.z - p1.z) - (p2.z - p1.z) * (p3.y - p1.y)
        self.B = (p2.z - p1.z) * (p3.x - p1.x) - (p2.x - p1.x) * (p3.z - p1.z)
        self.C = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
        self.D = -self.A * p1.x - self.B * p1.y - self.C * p1.z
        pass

    def is_inside(self, point):
        return self.A * point.x + self.B * point.y + self.C * point.z + self.D == 0

    def get_x(self, y, z):
        return -(self.B * y + self.C * z + self.D) / self.A

    def get_y(self, x, z):
        return -(self.A * x + self.C * z + self.D) / self.B

    def get_z(self, x, y):
        return -(self.A * x + self.B * y + self.D) / self.C


class Point:
    def __init__(self, loc):
        if loc is None:
            self.x, self.y, self.z = 0, 0, 0
        else:
            self.x, self.y, self.z = loc.toXYZ()

    @classmethod
    def create_point(cls, x, y, z):
        cls(None)
        cls.x = x
        cls.y = y
        cls.z = z
        return cls

    def get_distant(self, point):
        return math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2)

    @staticmethod
    def distant(point1, point2):
        return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2)


class Triangle:
    def __init__(self, loc1, loc2, loc3):
        if type(loc1) == type(Point):
            self.point1 = loc1
            self.point2 = loc2
            self.point3 = loc3
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
        self.sqare = math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def get_square(self):
        return self.sqare

    def is_inside(self, point):
        if point.x > self.max_x or point.x < self.min_x:
            return False
        if point.y > self.max_y or point.y < self.min_y:
            return False
        if point.z > self.max_z or point.z < self.min_z:
            return False
        if not self.area.is_inside(point):
            return False
        triangle1 = Triangle(point, self.point1, self.point2)
        triangle2 = Triangle(point, self.point2, self.point3)
        triangle3 = Triangle(point, self.point3, self.point1)
        if not self.sqare == triangle1.get_square() + triangle2.get_square() + triangle3.get_square():
            return False
        return True

    def get_point(self):
        while True:
            x = random.uniform(self.min_x, self.max_x)
            y = random.uniform(self.min_y, self.max_y)
            z = self.area.get_z(x, y)
            point = Point.create_point(x, y, z)
            if self.is_inside(point):
                return point

    def get_radius(self, point):
        triangle1 = Triangle(point, self.point1, self.point2)
        triangle2 = Triangle(point, self.point2, self.point3)
        triangle3 = Triangle(point, self.point3, self.point1)
        h1 = 2 * triangle1.get_square() / self.a
        h2 = 2 * triangle2.get_square() / self.b
        h3 = 2 * triangle3.get_square() / self.c
        return min(h1, h2, h3)
