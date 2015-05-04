#!/usr/bin/env python
# pylint: disable=R0904,R0901,C0103

"""
A TreeModel tailored for HDF
"""

# QtParts
from PySide import QtCore, QtGui

# HDF5 lib
import h5py

# prototype model
from .treeModel import TreeItem, TreeModel


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