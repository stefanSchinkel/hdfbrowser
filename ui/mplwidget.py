# pylint: disable=R0904,R0901,C0103
#!/usr/bin/env python
""" Class to provide an ad-hoc matplotlib canvas:
"""

from PySide import QtGui
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4'] = 'PySide'
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg \
import FigureCanvasQTAgg as FigureCanvas

class MPLCanvas(FigureCanvas):
    """A Canvas that we can put in Widget and the draw around
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """ Init with some reasonable defaults
        """
        # create axis
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        # init canvas
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)




