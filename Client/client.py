import matplotlib.backends.backend_agg as agg
import pylab
import pygame
import firebase_admin
from firebase_admin import credentials, firestore
import google.cloud.exceptions as gc_exceptions
from collections import deque
import matplotlib
matplotlib.use("Agg")


class LilypodFirestoreClient(object):
    # lily1 = Lilypod(name=u'aries', location=u'lake3', ph=5.4, conductivity=3.5, spectroscopy={'low': 1, 'high': 2})
    def __init__(self, credentialPath='Rpi/cloudcomm/privatekey/lilypod-7a62a-firebase-adminsdk-6odtt-737826cc07.json',
                 dbName=u'lilypods', lilypodName=u'lilypod_two'):
        cred = credentials.Certificate(credentialPath)
        self.app = firebase_admin.initialize_app(cred)
        db = firestore.client()
        self.dbRef = db.collection(dbName)
        self.lilypodName = lilypodName
        self.prevDoc = None

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

            # docRef = self.dbRef.document(docName)
            # doc = docRef.get()
            for doc in docs:
                if doc != self.prevDoc:
                    self.prevDoc = doc
                    return doc.to_dict()
                else:
                    return None
        except gc_exceptions.NotFound:
            print('DOC NOT FOUND')


class Chart():
    def __init__(self):
        self.surface = None
        self.location = None


class Dashboard():
    def __init__(self):
        pygame.init()
        self.lilypodFirestore = LilypodFirestoreClient()
        self.phMemory = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.condMemory = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.screen = None
        self.height = 800
        self.width = 1200
        self.title = None
        self.titlebox = None

    def generateEmptyDashboard(self):
        background_colour = (255, 255, 255)
        (width, height) = (self.width, self.height)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Lilypod Dashboard')
        self.screen.fill(background_colour)
        self.addTitle('Lilypod Dashboard')
        pygame.display.flip()

    def addTitle(self, title):
        font = pygame.font.Font('freesansbold.ttf', 50)
        self.title = font.render(title, True, (0, 0, 0), (255, 255, 255))
        self.titlebox = self.title.get_rect()
        self.titlebox.center = (self.width//2, self.height//15)

    def updateDashboard(self):
        running = True
        while running:
            self.screen.blit(self.title, self.titlebox)
            spectroscopyChartData = self.updateSpectroscopyData()
            phChartData = self.updatePhData()
            condChartData = self.updateCondData()
            if spectroscopyChartData is not None:
                spectroscopyChart = self.createChart('Spectrometry', spectroscopyChartData, 1)
                self.screen.blit(spectroscopyChart.surface, spectroscopyChart.location)
            if phChartData is not None:
                phChart = self.createChart('pH', phChartData, 2)
                self.screen.blit(phChart.surface, phChart.location)
            if condChartData is not None:
                condChart = self.createChart('Conductivity', condChartData, 3)
                self.screen.blit(condChart.surface, condChart.location)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()

    def createChart(self, title, data, loc):
        chart = Chart()
        fig = pylab.figure(figsize=[10, 2], dpi=100)
        ax = fig.gca()
        ax.plot(data['x'], data['y'], data['mark'])
        ax.set_title(title)
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        chart.surface = pygame.image.fromstring(raw_data, size, "RGB")
        chart.location = chart.surface.get_rect()
        chart.location.center = (self.width//2, loc*(self.height//4) + 20*loc)
        return chart

    def updateSpectroscopyData(self):
        spectroscopyData = self.getData('spectroscopy')
        if spectroscopyData is not None:
            spectroscopyKeys = list(spectroscopyData.keys())
            spectroscopyKeys = [int(i) for i in spectroscopyKeys]
            spectroscopyKeys.sort()
            spectroscopyKeys = [str(i) for i in spectroscopyKeys]
            spectroscopyVals = [spectroscopyData[k] for k in spectroscopyKeys]
            return {'x': spectroscopyKeys, 'y': spectroscopyVals, 'mark': 'bo-'}
        else:
            return None

    def updatePhData(self):
        phData = self.getData('ph')
        if phData is not None:
            self.phMemory.insert(0, phData)
            self.phMemory.pop()
            return {'x': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 'y': self.phMemory, 'mark': 'g+-'}
        else:
            return None

    def updateCondData(self):
        condData = self.getData('conductivity')
        if condData is not None:
            self.condMemory.insert(0, condData)
            self.condMemory.pop()
            return {'x': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 'y': self.condMemory, 'mark': 'rx-'}
        else:
            return None

    def getData(self, attribute):
        data = self.lilypodFirestore.read_from_db()
        if data is not None:
            return data[attribute]
        else:
            return None


def main():
    lilypodDashboard = Dashboard()
    lilypodDashboard.generateEmptyDashboard()
    lilypodDashboard.updateDashboard()
    # lilypodDashboard.getData('spectroscopy')


if __name__ == '__main__':
    main()
