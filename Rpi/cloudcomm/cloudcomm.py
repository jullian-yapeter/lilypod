import firebase_admin
from firebase_admin import credentials, firestore
import google.cloud.exceptions as gc_exceptions

from logs.logs import logs


class LilypodFirestore(object):
    # lily1 = Lilypod(name=u'aries', location=u'lake3', ph=5.4, conductivity=3.5, spectroscopy={'low': 1, 'high': 2})
    def __init__(self, credentialPath='cloudcomm/privatekey/lilypod-7a62a-firebase-adminsdk-6odtt-737826cc07.json',
                 dbName=u'lilypods'):
        cred = credentials.Certificate(credentialPath)
        self.app = firebase_admin.initialize_app(cred)
        db = firestore.client()
        self.dbRef = db.collection(dbName)

    def write_to_db(self, lilypodObject):
        self.dbRef.document(lilypodObject.name).set(lilypodObject.to_dict())
        logs.cloudcomm.info('%s WRITTEN TO DB', lilypodObject.name)
        return True

    def read_from_db(self, docName):
        try:
            docRef = self.dbRef.document(docName)
            doc = docRef.get()
            return doc.to_dict()
        except gc_exceptions.NotFound:
            logs.cloudcomm.warning('%s DOC NOT FOUND', docName)


class LilypodObject(object):
    def __init__(self, name, location, ph, conductivity, spectroscopy):
        self.name = name
        self.location = location
        self.ph = ph
        self.conductivity = conductivity
        self.spectroscopy = spectroscopy

    @staticmethod
    def from_dict(source):
        lilypodObject = LilypodObject(source[u'name'],
                                      source[u'loaction'],
                                      source[u'ph'],
                                      source[u'conductivity'],
                                      source[u'spectroscopy'])
        return lilypodObject

    def to_dict(self):
        dest = {
            u'name': self.name,
            u'location': self.location,
            u'ph': self.ph,
            u'conductivity': self.conductivity,
            u'spectroscopy': self.spectroscopy
        }
        return dest

    def __repr__(self):
        return(
            u'Lilypod(name={}, location={}, ph={}, conductivity={}, spectrscopy={})'
            .format(self.name, self.location, self.ph, self.conductivity, self.spectrscopy))
