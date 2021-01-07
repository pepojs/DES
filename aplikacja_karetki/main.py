# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, uic,QtCore,QtTest
from MainWindow import Ui_MainWindow
from Controller.controller import Controller
from Simulator.Simulator import Simulator, SimulatorSettings
from MessageController import MessageController
import numpy as np
import time

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self,onj=None,*args,**kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.messageController = MessageController()
        self.simSettings = SimulatorSettings()
        self.sim = Simulator(self.simSettings, self.messageController)
        self.con = Controller(self.simSettings, self.sim.hospitalsLocations(), self.messageController)
        self.ui.Mplwidget
        self.ui.Mplwidget.draw_hospital_on_map(self.con.Hospitals)
        self.ui.hospwidget
        self.ui.hospwidget.draw_all_hosp_inf(self.con.Hospitals)
        self.tablica_komunikatow=[]
        self.ui.start.clicked.connect(self.start_sim)
        self.ui.pauza.clicked.connect(self.stop_sim)
        self.ui.delay_time.setValue(50)
        self.ui.delay_time.valueChanged.connect(self.change_interval)
        self.timer = QtCore.QTimer(self, interval=self.ui.delay_time.value(), timeout=self.simulation)


    @QtCore.pyqtSlot()
    def start_sim(self):
        QtCore.QTimer.singleShot(0, self.simulation)
        self.timer.start()

    @QtCore.pyqtSlot()
    def stop_sim(self):
        self.timer.stop()

    def reset_sim(self):
        pass

    def change_interval(self):
        self.timer.setInterval(self.ui.delay_time.value())

    def simulation(self):
        self.sim.simulatorMianLoop(self.tablica_komunikatow)
        self.update_widgets_scrol()
        self.update_hospital_state(self.con.Hospitals)
        self.con.controllerMainLoop()

    def update_widgets_scrol(self):
        for elem in self.tablica_komunikatow:
            object = QLabel(elem)
            self.ui.verticalLayout_2.addWidget(object)
        self.tablica_komunikatow=[]

    def update_hospital_state(self,hospitals):
        index=self.ui.hospwidget.glayout.count()
#        print(self.ui.hospwidget.glayout.__dir__())
#        print('!!!!!!!!!!!!!!!')
#        print(self.ui.hospwidget.glayout.children()[0].__dir__())
#        print('!!!!!!!!!!!!!!!')
#        print(self.ui.hospwidget.glayout.children())
#        print('!!!!!!!!!!!!!!!')
#        print(self.ui.hospwidget.glayout.children()[0].itemAt(0).widget().__dir__())
#        print('!!!!!!!!!!!!!!!')
#        print(self.ui.hospwidget.glayout.children()[0].itemAt(0).widget())
#        print('!!!!!!!!!!!!!!!')
#        print(self.ui.hospwidget.glayout.children()[0].itemAt(0))
#        print('!!!!!!!!!!!!!!!')
#        print(self.ui.hospwidget.glayout.children()[0].itemAt(0).widget().text())
#        print('!!!!!!!!!!!!!!!')
        for i in range(len(hospitals)):
            count_ambulances = np.in1d(hospitals[i].ambulances, 6).sum()
            self.ui.hospwidget.glayout.children()[i].itemAt(1).widget().setText(str(count_ambulances))
            self.ui.hospwidget.glayout.children()[i].itemAt(2).widget().changecolor(hospitals[i].personnel)
            self.ui.hospwidget.glayout.children()[i].itemAt(3).widget().changecolor(hospitals[i].volume)
#            print('i {},personel {},miejsca {}'.format(i,hospitals[i].personnel,hospitals[i].volume))

#        firstwidget = self.ui.hospwidget.glayout.itemAt(3).objectName()
#        firstwidget.setText('hola')


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

#    window.ui.Mplwidget.draw_accident_on_map((250,250))
#    window.ui.Mplwidget.draw_accident_on_map((350,250))

#        print('!!!!!!!!!!!')
#        print(con.messageController.readAllObservableEvents())
#        print('!!!!!!!!!!!')
#        print(con.messageController.readAllControllableEvents())
#        print('!!!!!!!!!!!')
#        con.printState()
        #writ anything else to continue
#    window.update_hospital_state()
#    window.ui.Mplwidget.remove_accident_from_map((250,250))
#    window.ui.Mplwidget.ride_to_emergency(tuple(con.Hospitals[0].location), (350,250), 2, 10)
    app.exec_()


