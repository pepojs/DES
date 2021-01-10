# This Python file uses the following encoding: utf-8
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

class signalwidget(QWidget):
    def __init__(self,is_free=True):
        QWidget.__init__(self)
        self.color = QtGui.QColor(QtCore.Qt.green if is_free else QtCore.Qt.red)

    def paintEvent(self, event=None):
        paint=QtGui.QPainter(self)
        paint.setPen(QtGui.QPen(QtGui.QColor(self.color),1,QtCore.Qt.SolidLine))
        paint.setBrush(self.color)
        paint.drawEllipse(0,0, 20, 20)


    def changecolor(self,is_free=True):
        self.color=QtGui.QColor(QtCore.Qt.green if is_free else QtCore.Qt.red)
        self.update()

