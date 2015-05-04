#!/usr/bin/env python
# pylint: disable=R0904,R0901,C0103

"""
HDFViewer
=========

A simple viewer for HDF5 data

"""
# basics
import sys, os

# QtParts
from PySide import QtCore, QtGui

# Designer parts
from ui.layout import Ui_MainWindow

# Model and Items
from model.treeModel import TreeItem, TreeModel

# views
from views.data import DataViewer

# HDF5 lib
import h5py

# numpy and networkx for array handlin
# import numpy as np
# import networkx as nx

__version__ = "0.1"



class HDFModel(TreeModel):
    """ A data model for an HDF file, that is tied to a QTreeView
    """
    def __init__(self,fileName=None,parent=None):

        #init parent
        super(HDFModel, self).__init__(parent)

        # set file and update
        self.fileName=fileName

        self.setupData()
    ############################################################################
    ###                     START RE-IMPLEMENTATION                          ###
    ############################################################################
    def data(self, index, role):
        """ Re-mplementation of inherited data method (treeView.py/TreeModel)
        in order to fit the needs for HDF5 files.
        """

        #check basic validity
        if not index.isValid():
            return None

        # select current time
        item = index.internalPointer()

        # check if terminal or not
        flagIsTerminal = item.childCount() == 0

        if role == QtCore.Qt.ToolTipRole:
            return item.data(index.column())

        if role == QtCore.Qt.DecorationRole:
            if flagIsTerminal:
                icon = QtGui.QIcon(QtGui.QPixmap('icons/end.png'))
            else:
                icon = QtGui.QIcon(QtGui.QPixmap('icons/branch.png'))
            return icon

        if role == QtCore.Qt.DisplayRole:
            item = index.internalPointer()
            return item.data(index.column())

    ############################################################################
    ###                     END RE-IMPLEMENTATION                            ###
    ############################################################################
    def setupData(self):
        """Testing the HDFFile setup
        """
        # open HDF5 File
        self.fh = h5py.File(self.fileName)

        # simply set "header" and traverse the hierarchy
        self.rootItem = TreeItem(["Key"])
        self.traverseList(self.fh,self.rootItem)

        # alternatively on might add a slash at the beginning
        # and traverse then
        # self.rootItem = TreeItem(["Key"])
        # self.rootItem.appendChild(TreeItem(["/"],self.rootItem))
        # root = self.rootItem.child(0)
        # self.traverseList(self.fh,root)

    def traverseList(self,parent,branch):
        """ This function recursively traverses the
        HDF5 hierarchy and adds the corresponding branches
        and terminal nodes to the the model

       :param parent: a node of an HDF5 File
       :type parent: HDF5 Dataset or Group

       :param branch: a node in the model
       :type branch: TreeItem
        """
        #check if we have any children
        if self.isTerminal(parent):
            return

        # if so, iterate over keys and
        for child in parent.keys():
            # 1) add the current item to the current brach
            branch.appendChild(TreeItem([child],branch))

                # 2) if we have a terminal node, just continue
            if  self.isTerminal(parent[child]):
                self.traverseList(parent[child],branch)
            # otherwise add a branch at the current position
            # and set the branch for the next run accordingly
            else:
                idx = branch.childCount()
                self.traverseList(parent[child],branch.child(idx-1))

    def isTerminal(self,x):
        """ Determines whether a given treeitem is a terminal node,
        where everything that is not of type dataset is a non-terminal

        :return : if node is Terminal
        :rtype: bool
        """
        if x.__class__.__name__ == 'Dataset':
            return True
        else:
            return False

class HDFViewer(QtGui.QMainWindow, Ui_MainWindow):
    """ HDFViewer prototype -
    A simple GUI made in Desinger with a treeView and the HDFModel as a MV
    """
    def __init__(self, dataFile):
        # init super and load layout
        super(HDFViewer, self).__init__()
        self.setupUi(self)

        # assign callbacks (new-style)
        self.view.clicked.connect(self.itemSelected)
        self.view.doubleClicked.connect(self.wasDoubleClicked)
        self.actionOpen.activated.connect(self.updateModel)
        self.actionAbout.activated.connect(self.showAbout)

        # the plot Button should only be active if a dataset is selected!
        self.plotButton.clicked.connect(self.plotData)
        self.plotButton.setEnabled(False)

        # the same for the plotNetwork action
        # self.actionPlotNetwork.activated.connect(self.plotNetwork)
        self.plotButton.setEnabled(False)

        # init model if sth was passed in sys.arg
        if dataFile:
            self.updateModel(dataFile)

    def updateModel(self, dataFile=None):
        """ Update the model with a new file
        """
        # set or query for file to use in model
        dataFile = dataFile or QtGui.QFileDialog.getOpenFileName(
                    caption="Select .hdf file",
                    dir=os.getcwd(),
                    filter="HDF Files (*.hd5 *.hd4 *.hdf)",
                    )[0]

        if not dataFile:
            return

        # set model
        self.model = HDFModel(dataFile)
        self.view.setModel(self.model)
        self.statusbar.showMessage("Loaded %s" % self.model.fileName)

        # enable the potting of NW
        self.actionPlotNetwork.setEnabled(True)

    def showAbout(self):
        """ A simply about dialog, just to play with QMessageBox
        """
        QtGui.QMessageBox.about(self,
            "HDFViewer",
            """<b> HDFViewer Version %s</b>""" % (__version__))

    def itemSelected(self):
        """ Callback when a view item was selected, fills properties fields
        """

        # access the actual HDF item
        root = self.model.fh
        path = self.currentPath()
        self.hdfItem = root[path]

        if self.hdfItem.__class__.__name__ == 'Dataset':

            shape = self.hdfItem.shape
            if not len(shape):
                shapeStr = "scalar"
            else:
                shapeStr = str(self.hdfItem.shape)

            typeStr = str(self.hdfItem.dtype)
            # enable plotting  if dataset
            self.plotButton.setEnabled(True)

        else:
            shapeStr = "--"
            typeStr = "--"
            self.plotButton.setEnabled(False)


        self.sizeLabel.setText(shapeStr)
        self.typeLabel.setText(typeStr)

    def wasDoubleClicked(self):
        pass

    def currentPath(self):
        """ Return the path of the currently selected item

        :return: HDF path selected item
        :rtype: string
        """
        # get current item
        modelIndex = self.view.currentIndex()
        currentItem = modelIndex.parent()
        # traverse upwards to "/" and concat path on the way
        pathStr = ''
        while currentItem.row() != -1:
            pathStr = currentItem.data() + "/" + pathStr
            currentItem = currentItem.parent()

        return pathStr+modelIndex.data()

    def plotData(self):
        """ Plot the data currently selected on
        a newly instatiated MPLWidget window
        """

        # since this part can only be triggered for dataset items,
        # the current item (self.hdfItem) HAS to have shape etc pp
        # and we can savely pass it to the Viewer object
        self.DataViewer = DataViewer(parent=self,
                    data = self.hdfItem.value,
                    title = self.hdfItem.name)
        self.DataViewer.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    # def plotNetwork(self):
    #     """ Renders the network based on the admittance matrix
    #     This matrix is assumed to be in fh.keys()[0]/Amittance
    #     by definition. If the HDF5 format changes, remember to this
    #     function needs updating too.
    #     """
    #     # aquire admittance
    #     fh = self.model.fh
    #     x = fh[fh.keys()[0]+'/Admittance'].value

    #     # plot
    #     self.NetworkViewer = NetworkViewer(parent=self,
    #                 data = x,
    #                 title = "Network Layout")
    #     self.NetworkViewer.setAttribute(QtCore.Qt.WA_DeleteOnClose)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    try:
        dataFile = sys.argv[1]
    except IndexError:
        dataFile = ''

    win = HDFViewer(dataFile)
    win.show()
    win.raise_()
    sys.exit(app.exec_())
