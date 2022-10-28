from location import utils


class Location:
    def __init__(self, time, lat, lon, radius):
        self.t = time
        self.lat = lat
        self.lon = lon
        self.r = radius

    def __str__(self):
        return "时间：" + str(self.t) + "纬度：" + str(self.lat) + "经度：" + str(self.lon) + "半径：" + str(self.r)

    def enc(self, public_key):
        # self.lon, self.lat = wgs84_to_gcj02(self.lon, self.lat)
        x, y, z = utils.gcj02_to_coord(self.lon, self.lat)
        return encLocation(public_key, self.t, x, y, z, self.r)

    def toXYZ(self):
        x, y, z = utils.gcj02_to_coord(self.lon, self.lat)
        return x, y, z


class encLocation:
    def __init__(self, pk, time, x, y, z, radius):
        self.pk = pk
        self.t = time
        self.x = pk.encrypt(x)
        self.xx = pk.encrypt(x * x)
        self.y = pk.encrypt(y)
        self.yy = pk.encrypt(y * y)
        self.z = pk.encrypt(z)
        self.zz = pk.encrypt(z * z)
        self.r = radius
