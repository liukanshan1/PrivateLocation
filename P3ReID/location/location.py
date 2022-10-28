import utils


class Location:
    def __init__(self, time, lat, lon, radius):
        self.t = time
        self.lat = lat
        self.lon = lon
        self.r = radius

    def __str__(self):
        print("时间：", self.t, "纬度：", self.lat, "经度：", self.lon, "半径：", self.r)

    def enc(self, public_key):
        # self.lon, self.lat = wgs84_to_gcj02(self.lon, self.lat)
        x, y, z = utils.gcj02_to_coord(self.lon, self.lat)
        return encLocation(public_key, self.t, x, y, z, self.r)


class encLocation:
    def __init__(self, pk, time, x, y, z, radius):
        self.pk = pk
        self.t = time
        self.x = pk.encrypt(x)
        self.y = pk.encrypt(y)
        self.z = pk.encrypt(z)
        self.r = radius
