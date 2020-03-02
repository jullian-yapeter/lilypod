import numpy
import matplotlib as plt


class Graph():

    def __init__(self):
        self.xvals = []
        self.yvals = []

    def drawGraph(self):
        plt.scatter(self.xvals, self.yvals)

class 