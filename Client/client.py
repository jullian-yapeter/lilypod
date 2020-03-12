import time
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
        self.prevpredtimestamp = None

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

    def read_prediction(self):
        try:
            docRef = self.dbRef.document("prediction")
            doc = docRef.get()
            docdict = doc.to_dict()
            if docdict["time"] != self.prevpredtimestamp:
                self.prevpredtimestamp = docdict["time"]
                return docdict["value"]
        except gc_exceptions.NotFound:
            print('%s DOC NOT FOUND', self.lilypodName)

    def write_label(self, label):
        self.dbRef.document("label").set({"time": time.time(), "value": float(label)/100})
        print('LABEL WRITTEN TO DB')
        return True

    def write_command(self, command):
        self.dbRef.document("command").set({"time": time.time(), "value": command})
        print('LABEL WRITTEN TO DB')
        return True


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
        self.ii = InputInterface()
        self.currData = None

    def generateEmptyDashboard(self):
        background_colour = (220, 220, 220) #Light Grey
        (width, height) = (self.width, self.height)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('LILYPOD Dashboard')
        self.screen.fill(background_colour)
        self.addTitle('LILYPOD Dashboard')
        self.addLogo('logo.jpg')
        pygame.display.flip()

    def addTitle(self, title):
        font = pygame.font.Font('ostrich-regular.ttf', 90)
        self.title = font.render(title, True, (0, 0, 0), (220, 220, 220))
        self.titlebox = self.title.get_rect()
        self.titlebox.center = (self.width//2, self.height//15)

    def addLogo(self, logoImage):
        image = pygame.image.load(logoImage)
        image = pygame.transform.scale(image, (100,100))
        rect_image_bound = image.get_rect()
        rect_image_bound = rect_image_bound.move((self.width//8,self.height//120))
        self.screen.blit(image, rect_image_bound)

    def updateDashboard(self):
        running = True
        score = None
        while running:
            self.getData()
            spectroscopyChartData = self.updateSpectroscopyData()
            phChartData = self.updatePhData()
            condChartData = self.updateCondData()
            if spectroscopyChartData is not None:
                spectroscopyChart = self.createChart('Spectrometry', spectroscopyChartData, 1)
                self.screen.blit(spectroscopyChart.surface, spectroscopyChart.location)
            else:
                print("SPEC NONE")
            if phChartData is not None:
                phChart = self.createChart('pH', phChartData, 2)
                self.screen.blit(phChart.surface, phChart.location)
            else:
                print("PH NONE")
            if condChartData is not None:
                condChart = self.createChart('Conductivity', condChartData, 3)
                self.screen.blit(condChart.surface, condChart.location)
            else:
                print("COND NONE")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if self.ii.input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        self.ii.active = not self.ii.active
                    else:
                        self.ii.active = False

                    if self.ii.label_button.collidepoint(event.pos):
                        # Toggle the active variable.
                        self.ii.lb_active = True
                    else:
                        self.ii.lb_active = False

                    if self.ii.predict_button.collidepoint(event.pos):
                        # Toggle the active variable.
                        self.ii.pb_active = True
                    else:
                        self.ii.pb_active = False
                    # Change the current color of the input box.
                    self.ii.color = self.ii.color_active if self.ii.active else self.ii.color_inactive

                if self.ii.lb_active:
                    try:
                        self.lilypodFirestore.write_label(self.ii.text)
                        self.screen.fill(pygame.Color("white"), self.ii.input_box)
                        self.ii.text = ''
                        self.ii.lb_active = False
                    except:
                        print("INPUT WAS INVALID")
                        pass

                if self.ii.pb_active:
                    try:
                        self.lilypodFirestore.write_command(True)
                        self.screen.fill(pygame.Color("white"), self.ii.output_box)
                        time.sleep(1)
                        score = self.lilypodFirestore.read_prediction()
                        self.ii.pb_active = False
                    except:
                        print("FAILED GETTING PREDICTION")
                        pass

                if event.type == pygame.KEYDOWN:
                    if self.ii.active:
                        if event.key == pygame.K_RETURN:
                            print(self.ii.text)
                            # self.ii.text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            self.screen.fill(pygame.Color("white"), self.ii.input_box)
                            self.ii.text = self.ii.text[:-1]
                        else:
                            self.ii.text += event.unicode

            txt_surface = self.ii.font.render(self.ii.text, True, self.ii.color)
            output_txt_surface = None
            if score is not None:
                output_txt_surface = self.ii.font.render(str(round(score, 2)), True, pygame.Color('black'))

            label_txt_surface = self.ii.font.render("Set Rating", True, pygame.Color('black'))
            predict_txt_surface = self.ii.font.render("Get Rating", True, pygame.Color('black'))

            width = max(200, txt_surface.get_width()+10)

            self.screen.blit(self.title, self.titlebox)
            self.screen.blit(self.ii.labelboxtitle, self.ii.labelboxtitlebox)
            self.screen.blit(self.ii.scoreboxtitle, self.ii.scoreboxtitlebox)

            self.ii.input_box.w = width
            self.screen.blit(txt_surface, (self.ii.input_box.x+10, self.ii.input_box.y+10))
            pygame.draw.rect(self.screen, self.ii.color, self.ii.input_box, 2)

            if output_txt_surface is not None:
                self.screen.blit(output_txt_surface, (self.ii.output_box.x+10, self.ii.output_box.y+10))
            pygame.draw.rect(self.screen, pygame.Color('green'), self.ii.output_box, 2)

            pygame.draw.rect(self.screen, pygame.Color('lightblue'), self.ii.label_button, 0)
            self.screen.blit(label_txt_surface, (self.ii.label_button.x+50, self.ii.label_button.y+5))

            pygame.draw.rect(self.screen, pygame.Color('lightgreen'), self.ii.predict_button, 0)
            self.screen.blit(predict_txt_surface, (self.ii.predict_button.x+50, self.ii.predict_button.y+5))

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
        chart.location.center = (self.width//2 - 120, loc*(self.height//4) + 20*loc)
        return chart

    def updateSpectroscopyData(self):
        # print(self.currData)
        spectroscopyData = self.currData['spectroscopy']
        if spectroscopyData is not None:
            spectroscopyKeys = list(spectroscopyData.keys())
            spectroscopyKeys = [float(i) for i in spectroscopyKeys]
            spectroscopyKeys.sort()
            spectroscopyKeys = [str(i) for i in spectroscopyKeys]
            spectroscopyVals = [spectroscopyData[k] for k in spectroscopyKeys]
            return {'x': spectroscopyKeys, 'y': spectroscopyVals, 'mark': 'bo-'}
        else:
            return None

    def updatePhData(self):
        phData = self.currData['ph']
        if phData is not None:
            self.phMemory.insert(0, phData)
            self.phMemory.pop()
            return {'x': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 'y': self.phMemory, 'mark': 'g+-'}
        else:
            return None

    def updateCondData(self):
        condData = self.currData['conductivity']
        if condData is not None:
            self.condMemory.insert(0, condData)
            self.condMemory.pop()
            return {'x': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 'y': self.condMemory, 'mark': 'rx-'}
        else:
            return None

    def getData(self):
        data = self.lilypodFirestore.read_from_db()
        if data is not None:
            self.currData = data
            return data
        else:
            return None


class InputInterface():
    def __init__(self):
        self.input_box = pygame.Rect(940, 200, 200, 32)
        self.active = False
        self.text = ''
        self.font = pygame.font.Font(None, 32)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive

        self.output_box = pygame.Rect(940, 400, 200, 32)

        self.label_button = pygame.Rect(940, 250, 200, 32)
        self.lb_active = False

        self.predict_button = pygame.Rect(940, 450, 200, 32)
        self.pb_active = False

        font = pygame.font.Font('ostrich-regular.ttf', 30)
        self.labelboxtitle = font.render("Input Crop Rating", True, (0, 0, 0), (220, 220, 220))
        self.labelboxtitlebox = self.labelboxtitle.get_rect()
        self.labelboxtitlebox.center = (self.input_box.center[0], self.input_box.center[1]-30)

        self.scoreboxtitle = font.render("Predicted Crop Rating", True, (0, 0, 0), (220, 220, 220))
        self.scoreboxtitlebox = self.scoreboxtitle.get_rect()
        self.scoreboxtitlebox.center = (self.output_box.center[0], self.output_box.center[1]-30)

def main():
    lilypodDashboard = Dashboard()
    lilypodDashboard.generateEmptyDashboard()
    lilypodDashboard.updateDashboard()
    # lilypodDashboard.getData('spectroscopy')


if __name__ == '__main__':
    main()
