import geocoder


class Geolocation():
    def getGeolocation():
        g = geocoder.ip('me')
        return g.latlng
