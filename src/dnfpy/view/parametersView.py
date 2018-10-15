from PyQt5 import QtWidgets
import sip

class ParametersView(QtWidgets.QWidget):
    def __init__(self,runner):
        super(ParametersView,self).__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
    	self.__nbWidg = 0
    	self.setMaximumWidth(0)
        self.widgetDict = {}

    def addWidget(self,name,widget):
    	if self.__nbWidg == 0:
	    	self.setMaximumWidth(300)
    	self.__nbWidg += 1
        self.layout.addWidget(widget)
        self.widgetDict.update({name:widget})

    def removeWidget(self,name):
        widg = self.widgetDict[name]
        #self.layout.removeWidget(widg)
        self.__nbWidg -= 1
    	if self.__nbWidg == 0:
	    	self.setMaximumWidth(0)





