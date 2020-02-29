import geocoder


class Geolocation():
    def getGeolocation(self):
        g = geocoder.ip('me')
        return g.latlng
