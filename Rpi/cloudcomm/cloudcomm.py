import firebase_admin
from firebase_admin import credentials, firestore
import google.cloud.exceptions as gc_exceptions

# from logs.logs import logs


class LilypodFirestore(object):
    # lily1 = Lilypod(name=u'aries', location=u'lake3', ph=5.4, conductivity=3.5, spectroscopy={'low': 1, 'high': 2})
    def __init__(self, credentialPath='Rpi/cloudcomm/privatekey/lilypod-7a62a-firebase-adminsdk-fakekey.json',
                 dbName=u'lilypods'):
        cred = credentials.Certificate(credentialPath)
        self.app = firebase_admin.initialize_app(cred)
        db = firestore.client()
        self.dbRef = db.collection(dbName)

    def write_to_db(self, lilypodObject):
        self.dbRef.document(str(lilypodObject.timestamp)).set(lilypodObject.to_dict())
        # logs.cloudcomm.info('%s WRITTEN TO DB', lilypodObject.timestamp)
        return True

    # def read_from_db(self):
    #     try:
    #         docRef = self.dbRef.document(self.lilypodName)
    #         doc = docRef.get()
    #         return doc.to_dict()
    #     except gc_exceptions.NotFound:
    #         print('%s DOC NOT FOUND', self.lilypodName)
    
    def read_from_db(self):
        try:
            docRef = self.dbRef.order_by(u'timestamp',
                                         direction=firestore.Query.DESCENDING).limit(1)
            docs = docRef.stream()
            for doc in docs:
                return doc.to_dict()
        except gc_exceptions.NotFound:
            # logs.cloudcomm.warning('DOC NOT FOUND')
            pass


class LilypodObject(object):
    def __init__(self, name, timestamp, location, ph, conductivity, garbageLevel, spectroscopy):
        self.name = name
        self.timestamp = timestamp
        self.location = location
        self.ph = ph
        self.conductivity = conductivity
        self.garbageLevel = garbageLevel
        self.spectroscopy = spectroscopy

    @staticmethod
    def from_dict(source):
        lilypodObject = LilypodObject(source[u'name'],
                                      source[u'timestamp'],
                                      source[u'location'],
                                      source[u'ph'],
                                      source[u'conductivity'],
                                      source[u'garbageLevel'],
                                      source[u'spectroscopy'])
        return lilypodObject

    def to_dict(self):
        dest = {
            u'name': self.name,
            u'timestamp': self.timestamp,
            u'location': self.location,
            u'ph': self.ph,
            u'conductivity': self.conductivity,
            u'garbageLevel': self.garbageLevel,
            u'spectroscopy': self.spectroscopy
        }
        return dest

    def __repr__(self):
        return(
            u'Lilypod(name={}, timestamp={}, location={}, ph={}, conductivity={}, garbageLevel={}, spectrscopy={})'
            .format(self.name, self.timestamp, self.location, self.ph, self.conductivity, self.garbageLevel, self.spectrscopy))


if __name__ == '__main__':
    import time
    lpod = LilypodObject('test', time.time(), [0.0, 0.0], 7.0, 2.0, 0.0, {"0": 1, "1": 2, "2": 3, "3": 4, "4": 5, "5": 6, "6": 7, "8": 9, "9": 10})
    lf = LilypodFirestore()
    lf.write_to_db(lpod)
    result = lf.read_from_db()
    print(result)
