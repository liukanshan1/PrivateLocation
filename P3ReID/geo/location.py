from geo import utils


class Location:
    def __init__(self, time, lat, lon, radius, neg=False):
        self.t = time
        self.lat = lat
        self.lon = lon
        self.r = radius
        self.neg = neg

    def __str__(self):
        return "时间：" + str(self.t) + "纬度：" + str(self.lat) + "经度：" + str(self.lon) + "半径：" + str(self.r)

    def enc(self, public_key):
        # self.lon, self.lat = wgs84_to_gcj02(self.lon, self.lat)
        x, y, z = self.toXYZ()
        return encLocation(public_key, self.t, x, y, z, self.r, self.neg)

    def toXYZ(self):
        return utils.gcj02_to_coord(self.lon, self.lat)


class encLocation:
    def __init__(self, pk, time, x, y, z, radius, neg=False):
        self.pk = pk
        self.t = time
        if neg:
            x = -x
            y = -y
            z = -z
            x = round(x)
            y = round(y)
            z = round(z)
            self.x = pk.encrypt(x * 2)
            self.y = pk.encrypt(y * 2)
            self.z = pk.encrypt(z * 2)
        else:
            x = round(x)
            y = round(y)
            z = round(z)
            self.x = pk.encrypt(x)
            self.y = pk.encrypt(y)
            self.z = pk.encrypt(z)
        self.xx = pk.encrypt(x * x)
        self.yy = pk.encrypt(y * y)
        self.zz = pk.encrypt(z * z)
        self.r = radius
