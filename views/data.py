#!/usr/bin/env python
# pylint: disable=R0904,R0901,C0103

# QtParts
from PySide import QtCore, QtGui

# MPL
from ui.mplwidget import  MPLCanvas

# numpy and networkx for array handlin
import networkx as nx

class NetworkViewer(QtGui.QWidget):
    """ Simple Widget that plots the provided data as a networkx graph
    """

    def __init__(self, parent = None, data = None, title = None):
        super(NetworkViewer, self).__init__()

        self.canvas = MPLCanvas(parent=self)
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

        # # set up for title String
        self.title = title or  " Network topography"
        self.canvas.axes.set_title(self.title)

        self.setWindowTitle(self.title)
        # render graph and draw
        G = nx.from_numpy_matrix(data)
        nx.draw_networkx(G, ax=self.canvas.axes)

        # show everything
        self.canvas.axes.axis('off')
        self.canvas.show()
        self.show()

class DataViewer(QtGui.QWidget):
    """ Simple Widget that plots the provided data as simple lines graphics.
    """

    def __init__(self, parent = None, data = None, title = None):
        super(DataViewer, self).__init__()

        # a simple plot can only deal w/ 1D and 2D data
        # thus we query for that
        if data is None or not (1 <= len(data.shape) <= 2):
            print "Cant cont. shape is %s" % str(data.shape)
            return

        self.canvas = MPLCanvas(parent=self)
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

        # set up for title String
        self.title = title or  " This is data!"

        self.setWindowTitle(self.title)
        self.canvas.axes.set_title(self.title)
        self.canvas.axes.plot(data)
        self.canvas.draw()
        self.show()