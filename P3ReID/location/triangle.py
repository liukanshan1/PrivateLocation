import math
import random


class Area:
    def __init__(self, p1, p2, p3):
        self.A = (p2.y - p1.y) * (p3.z - p1.z) - (p2.z - p1.z) * (p3.y - p1.y)
        self.B = (p2.z - p1.z) * (p3.x - p1.x) - (p2.x - p1.x) * (p3.z - p1.z)
        self.C = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
        self.D = -self.A * p1.x - self.B * p1.y - self.C * p1.z

    def is_inside(self, point):
        return self.A * point.x + self.B * point.y + self.C * point.z + self.D == 0

    def get_x(self, y, z):
        return -(self.B * y + self.C * z + self.D) / self.A

    def get_y(self, x, z):
        return -(self.A * x + self.C * z + self.D) / self.B

    def get_z(self, x, y):
        return -(self.A * x + self.B * y + self.D) / self.C

    def __str__(self):
        return "A: " + str(self.A) + " B: " + str(self.B) + " C: " + str(self.C) + " D: " + str(self.D)


class Point:
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
        triangle1 = Triangle.create_triangle(self.point1, self.point2, point)
        triangle2 = Triangle.create_triangle(self.point2, self.point3, point)
        triangle3 = Triangle.create_triangle(self.point3, self.point1, point)
        h1 = 2 * triangle1.get_square() / self.a
        h2 = 2 * triangle2.get_square() / self.b
        h3 = 2 * triangle3.get_square() / self.c
        return min(h1, h2, h3)

    def get_circle(self, num):
        result = []
        for i in range(num):
            point = self.get_point()
            radius = self.get_radius(point)
            result.append([point, radius])
        return result


if __name__ == '__main__':
    p1 = Point.create_point(1, 0, 0)
    p2 = Point.create_point(0, 1, 0)
    p3 = Point.create_point(0, 0, 1)
    print(p1.get_distant(p2))
    print(Point.distant(p1, p2))
    area = Area(p1, p2, p3)
    print(area.get_x(0.5, 0.5))
    print(area.get_y(0.5, 0.5))
    print(area.get_z(0.5, 0.5))
    print(area.is_inside(Point.create_point(0.5, 0.5, 0)))
    triangle = Triangle.create_triangle(p1, p2, p3)
    print(triangle.get_square())
    print(triangle.is_inside(Point.create_point(0.5, 0.5, 0)))
    pp = triangle.get_point()
    print(triangle.get_point())
    print(triangle.is_inside(pp))
    print(triangle.get_radius(pp))
    print(triangle.get_circle(10))


