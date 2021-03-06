from collections import OrderedDict
import sip
from PyQt5 import QtWidgets,  QtCore
from PyQt5.QtCore import pyqtSlot
import math
import numpy as np
from view import View
from parametersView import ParametersView
from mapView import ArrayWidget


class GlobalParams(QtWidgets.QWidget):
        """
            Global parameter of the runner
        """
        def __init__(self, runner):
            super(GlobalParams, self).__init__()

            self.runner = runner
            layout = QtWidgets.QHBoxLayout(self)
            bSaveFig = QtWidgets.QPushButton("Save Figures")
            bSaveFig.clicked.connect(runner.saveFigSlot)
            bSaveArr = QtWidgets.QPushButton("Save Data")
            bSaveArr.clicked.connect(runner.saveArrSlot)
            bPlay = QtWidgets.QPushButton("Play/Pause")
            bPlay.clicked.connect(runner.playSlot)
            bStep = QtWidgets.QPushButton("Step")
            bStep.clicked.connect(runner.stepSlot)
            spinSpeedRatio = QtWidgets.QDoubleSpinBox()
            spinSpeedRatio.setMinimum(0.0)
            spinSpeedRatio.setMaximum(10.0)
            spinSpeedRatio.setValue(runner.getTimeRatio())
            spinSpeedRatio.setSingleStep(0.1)
            spinSpeedRatio.setDecimals(1)
            spinSpeedRatio.valueChanged.connect(runner.setTimeRatio)
            spinSpeedRatio.setPrefix("Speed : ")

            layout.addWidget(bSaveFig)
            layout.addWidget(bSaveArr)
            layout.addWidget(bPlay)
            layout.addWidget(bStep)
            layout.addWidget(spinSpeedRatio)


class DisplayModelQt(QtWidgets.QWidget, View):
    def __init__(self, renderable):
        super(DisplayModelQt,  self).__init__()
        self.widgetV = QtWidgets.QWidget()
        self.layoutV = QtWidgets.QVBoxLayout(self.widgetV)

        self.layoutH = QtWidgets.QHBoxLayout(self)
        self.renderable = renderable

        self.setGeometry(0,  0,  1000,  700)


    #Override View
    def setRunner(self, runner):
        self.runner = runner
        self.globalParams = GlobalParams(self.runner)
        self.rightPanel = ParametersView(self.runner)
        self.displayMaps = DisplayMapsQt(self.renderable,self.runner,self.rightPanel)
        self.layoutV.addWidget(self.displayMaps)
        self.layoutV.addWidget(self.globalParams)

        self.layoutH.addWidget(self.widgetV)
        self.layoutH.addWidget(self.rightPanel)

    #Override View
    @pyqtSlot()
    def update(self):
        self.displayMaps.update()
        self.repaint()


    #Override View
    @pyqtSlot(str)
    def updateParams(self,mapName):
        self.displayMaps.updateParams(str(mapName))



class DisplayMapsQt(QtWidgets.QWidget):
    """

    """

    def __init__(self, renderable, runner,parametersView):
        super(DisplayMapsQt,  self).__init__()
        self.renderable = renderable
        self.parametersView = parametersView
        self.runner = runner
        size = len(self.renderable.getArrays())
        self.simuTime = 0

        self.dictLabels = OrderedDict()
        self.grid = QtWidgets.QGridLayout(self)
        self.__updateGridSize(size)


        #debug
        self.paintEventCount = 0
        self.mapUpdate = 0

        self.__initArrays()

    def __updateGridSize(self,size):
        self.size = size
        self.nbCols = int(math.ceil(math.sqrt(size))) #nb cols in the label matrix
        self.nbRows = int(math.ceil(size/float(self.nbCols))) #nb rows in the label matrix




    def __initArrays(self):
        """
            Add all arrays of renderable
        """
        maps = self.renderable.getArrays()
        for map in maps:
            self.addMap( map)

    @pyqtSlot(str)
    def addChildrenMap(self,mapName):
        """
        Add a map to the view when clicked on children map button
        """
        mapName = str(mapName)
        map = self.renderable.getMap(mapName)
        if mapName in self.dictLabels.keys():
            self.removeMap(mapName)
            self.__updateGridSize(self.size-1)
            self.__reorganizeGrid()
        else:
            self.__updateGridSize(self.size+1)
            self.addMap(map)
            self.__reorganizeGrid()

    def __placeWidgetOnGrid(self,index,widg):
        row = index / self.nbCols
        col = index % self.nbCols
        self.grid.addWidget(widg, row, col)
        
    def __reorganizeGrid(self):
        for label in self.dictLabels.values():
            self.grid.removeWidget(label)

        i = 0
        for label in self.dictLabels.values():
            self.__placeWidgetOnGrid(i,label)
            i += 1






    def addMap(self,  map_):
        """
            Add a new map to the view
            return the index of the map
        """
        label = ArrayWidget(map_,self.runner,self.parametersView,self)
        self.dictLabels.update({map_.getName():label})
        index = len(self.dictLabels)-1
        self.__placeWidgetOnGrid(index,label)
        label.setVisible(True)

    def removeMap(self,mapName):
        label = self.dictLabels[mapName]
        sip.delete(label)
        label = None
        del self.dictLabels[mapName]

    def update(self):
        """
            The controller will send a update signal to say that a map changed
            The map ids to update will be stored in idsToUpdate
            The map itself will be in mapToUpdate in the same order
        """
        for mapName in self.dictLabels:
            self.dictLabels[mapName].updateArray()


        self.mapUpdate += 1

    def updateParams(self,mapName):
            label = self.dictLabels[mapName]
            label.onParamsChanged()
