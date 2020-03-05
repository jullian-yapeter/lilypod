import numpy as np
from lilymodel import LilypodML
import firebase_admin
from firebase_admin import credentials, firestore
import google.cloud.exceptions as gc_exceptions
import time


class LilypodFirestoreServer(object):

    def __init__(self, credentialPath='Rpi/cloudcomm/privatekey/lilypod-7a62a-firebase-adminsdk-6odtt-737826cc07.json',
                 dbName=u'lilypods', lilypodName=u'lilypod_two'):
        cred = credentials.Certificate(credentialPath)
        self.app = firebase_admin.initialize_app(cred)
        db = firestore.client()
        self.dbRef = db.collection(dbName)
        self.lilypodName = lilypodName
        self.prevDoc = None

    def read_from_db(self):
        try:
            docRef = self.dbRef.order_by(u'timestamp',
                                         direction=firestore.Query.DESCENDING).limit(1)
            docs = docRef.stream()
            for doc in docs:
                if doc != self.prevDoc:
                    self.prevDoc = doc
                    return doc.to_dict()
                else:
                    return None
        except gc_exceptions.NotFound:
            print('DOC NOT FOUND')

    def read_score(self):
        try:
            docRef = self.dbRef.document("label")
            doc = docRef.get()
            return doc.to_dict()
        except gc_exceptions.NotFound:
            print('SCORE DOC NOT FOUND')

    def read_command(self):
        try:
            docRef = self.dbRef.document("command")
            doc = docRef.get()
            return doc.to_dict()
        except gc_exceptions.NotFound:
            print('SCORE DOC NOT FOUND')

    def write_prediction(self, prediction):
        self.dbRef.document("prediction").set({"time": time.time(), "value": prediction})
        print('PREDICTION WRITTEN TO DB')
        return True

    def reset_command(self):
        self.dbRef.document("command").set({"time": time.time(), "value": False})
        print('COMMAND RESET')
        return True


class OnlineLearn():

    def __init__(self):
        self.currData = None
        self.lilypodFirestore = LilypodFirestoreServer()
        self.lilypodModel = LilypodML()
        self.lilypodModel.resetStates()
        self.prevtimestamp = None
        self.prevcommandtimestamp = None

    def updateModel(self):
        self.getData()
        spectroscopyChartData = self.updateSpectroscopyData()
        phChartData = self.updatePhData()
        condChartData = self.updateCondData()
        if (spectroscopyChartData is not None) and (phChartData is not None) and (condChartData is not None):
            label = self.lilypodFirestore.read_score()
            if label["time"] != self.prevtimestamp:
                print("IN_UPDATE")
                # data = self.lilypodFirestore.read_from_db()
                # print(data)
                # if self.currData is not None:
                self.prevtimestamp = label["time"]
                x_data = [spectroscopyChartData, phChartData, condChartData]
                print(x_data)
                # print(x_data)
                self.lilypodModel.fitModel(10, x_data, np.array([[[label["value"]]]]))

    def updateSpectroscopyData(self):
        spectroscopyData = self.currData['spectroscopy']
        if spectroscopyData is not None:
            spectroscopyKeys = list(spectroscopyData.keys())
            spectroscopyKeys = [int(i) for i in spectroscopyKeys]
            spectroscopyKeys.sort()
            spectroscopyKeys = [str(i) for i in spectroscopyKeys]
            spectroscopyVals = [spectroscopyData[k] for k in spectroscopyKeys]
            return np.array([[spectroscopyVals]])

    def updatePhData(self):
        phData = self.currData['ph']
        if phData is not None:
            return np.array([[[phData]]])

    def updateCondData(self):
        condData = self.currData['conductivity']
        if condData is not None:
            return np.array([[[condData]]])

    def getData(self):
        data = self.lilypodFirestore.read_from_db()
        if data is not None:
            self.currData = data
            # print(self.currData)
            return data
        else:
            return None

    def predictCropScore(self):
        self.getData()
        spectroscopyChartData = self.updateSpectroscopyData()
        phChartData = self.updatePhData()
        condChartData = self.updateCondData()
        if (spectroscopyChartData is not None) and (phChartData is not None) and (condChartData is not None):
            command = self.lilypodFirestore.read_command()
            if (command["time"] != self.prevcommandtimestamp) and command["value"]:
                print("IN_PREDICT")
                # data = self.lilypodFirestore.read_from_db()
                # if data is not None:
                self.lilypodFirestore.reset_command()
                self.prevcommandtimestamp = command["time"]
                x_data = [spectroscopyChartData, phChartData, condChartData]
                print(x_data)
                score = self.lilypodModel.predictScore(x_data)
                self.lilypodFirestore.write_prediction(min(100, max(0, float(score[0][0])*100) ) )
                return float(score[0][0])*100


if __name__ == '__main__':
    lilyLearn = OnlineLearn()
    while True:
        lilyLearn.updateModel()
        score = lilyLearn.predictCropScore()
        if score is not None:
            print(score)
