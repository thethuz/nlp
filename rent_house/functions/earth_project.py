import math


class EarthProject(object):

    R = 6378137
    MAX_LATITUDE = 85.0511287798

    def __init__(self, unit):
        super(EarthProject, self).__init__()
        self.unit = unit

    def project(self, latlng):
        d = math.pi / 180
        maxL = self.MAX_LATITUDE
        lat = max(min(maxL, latlng['lat']), -maxL)
        sin = math.sin(lat * d)

        return {'x': math.floor(self.R * latlng['lng'] * d / self.unit), 'y': math.floor(self.R * math.log((1 + sin) / (1 - sin)) / 2 / self.unit)}

    def unproject(self, point):
        d = 180 / math.pi
        return {u'lat': (2 * math.atan(math.exp(point['y'] * self.unit / self.R)) - (math.pi / 2)) * d, u'lng': point['x'] * self.unit * d / self.R}

    def distance(self, dlat1, dlon1, dlat2, dlon2):
        lat1 = math.radians(dlat1)
        lon1 = math.radians(dlon1)
        lat2 = math.radians(dlat2)
        lon2 = math.radians(dlon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return math.floor(self.R * c)