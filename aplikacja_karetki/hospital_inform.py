# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import sys
from signalwidget import signalwidget
import numpy as np

class hospital_inform(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self, parent)
#        self.glayout = QGridLayout()
        self.glayout = QVBoxLayout()
#        self.color1 = QtGui.QColor(QtCore.Qt.green)
#        self.glayout.setVerticalSpacing(0)
#        self.glayout.setSpacing(0)
        self.glayout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.glayout)
        self.show()
#        self.bt.clicked.connect(self.changecolor)

    def draw_hosp_inf(self,id,ambulances,place,personel):
        layout1=QHBoxLayout()
        free_place = signalwidget(place)
        free_personel = signalwidget(personel)
        l1=QLabel(str(id))
        l2=QLabel(str(ambulances))
        font = QtGui.QFont()
        font.setPointSize(14)
        l1.setFont(font)
        l2.setFont(font)
#        self.glayout.addWidget(l1,0,0,1,1,QtCore.Qt.AlignTop)
#        self.glayout.addWidget(l2,0,1,1,1,QtCore.Qt.AlignTop)
#        self.glayout.addWidget(self.free_place,0,2,1,1)
#        self.glayout.addWidget(self.free_personel,0,3,1,1)
        layout1.addWidget(l1)
        layout1.addWidget(l2)
        layout1.addWidget(free_place)
        layout1.addWidget(free_personel)
        self.glayout.addLayout(layout1)

    def draw_all_hosp_inf(self,hospitals):
        for i in range(len(hospitals)):
            count_ambulances = np.in1d(hospitals[i].ambulances, 6).sum()
            self.draw_hosp_inf(i+1,count_ambulances,hospitals[i].volume,hospitals[i].personnel)

    def clean_all_hosp_inf(self):
        self.deleteItemsOfLayout(self.glayout)

    def deleteItemsOfLayout(self,layout):
         if layout is not None:
             while layout.count():
                 item = layout.takeAt(0)
                 widget = item.widget()
                 if widget is not None:
                     widget.setParent(None)
                 else:
                     self.deleteItemsOfLayout(item.layout())

    def changecolor(self):
        self.color = QtGui.QColor(QtCore.Qt.red)
        self.update()


#app=QtWidgets.QApplication(sys.argv)
#f=hospital_inform()
#f.show()
#app.exec_()
