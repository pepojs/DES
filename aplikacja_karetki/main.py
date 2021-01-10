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
        self.control_events=[]
        self.observ_from_message=[]
        self.ui.start.clicked.connect(self.start_sim)
        self.ui.pauza.clicked.connect(self.stop_sim)
        self.ui.reset.clicked.connect(self.reset_sim)
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
        del self.messageController
        del self.simSettings
        del self.sim
        del self.con
        self.ui.Mplwidget.clean_hospital_on_map()
        self.ui.hospwidget.clean_all_hosp_inf()
        self.clear_widget_scrol()
        self.messageController = MessageController()
        self.simSettings = SimulatorSettings()
        self.sim = Simulator(self.simSettings, self.messageController)
        self.con = Controller(self.simSettings, self.sim.hospitalsLocations(), self.messageController)
        self.ui.Mplwidget.draw_hospital_on_map(self.con.Hospitals)
        self.ui.hospwidget.draw_all_hosp_inf(self.con.Hospitals)

    def change_interval(self):
        self.timer.setInterval(self.ui.delay_time.value())

    def simulation(self):
        self.sim.simulatorMianLoop(self.tablica_komunikatow,self.control_events)
        if self.messageController.readAllObservableEventsForSimulation():
            self.observ_from_message.append(self.messageController.readAllObservableEventsForSimulation())

        if len(self.observ_from_message)>0:
            for event in self.observ_from_message:
                if event[0][0] == 'E1o':
                    self.ui.Mplwidget.draw_accident_on_map(tuple(event[0][1][0]))
                    self.observ_from_message.remove(event)
                elif event[0][0] == 'E5o':
                    self.ui.Mplwidget.remove_car_from_map((self.con.Hospitals[event[0][1][0]-1].location[0]+1,self.con.Hospitals[event[0][1][0]-1].location[1]+1))
                    self.ui.Mplwidget.draw_car_on_map(tuple(event[0][1][2]))

                    self.observ_from_message.remove(event)
                elif event[0][0] == 'E7o':
                    self.ui.Mplwidget.draw_car_on_map((self.con.Hospitals[event[0][1][0]-1].location[0]+1,self.con.Hospitals[event[0][1][0]-1].location[1]+1))
                    self.observ_from_message.remove(event)
                elif event[0][0] == 'E8o':
                    self.ui.Mplwidget.remove_car_from_map((self.con.Hospitals[event[0][1][0]-1].location[0]+1,self.con.Hospitals[event[0][1][0]-1].location[1]+1))
                    self.observ_from_message.remove(event)
                else:
                    self.observ_from_message.remove(event)


        if len(self.control_events)>0:
            for event in self.control_events:
#                print('control', event)
                if event[0][0] == 'E1c':
                    self.ui.Mplwidget.draw_car_on_map((self.con.Hospitals[event[0][1][0]-1].location[0]+1,self.con.Hospitals[event[0][1][0]-1].location[1]+1))
                    self.control_events.remove(event)
                elif event[0][0] == 'E2c':
                    self.ui.Mplwidget.remove_accident_from_map(tuple(event[0][1][1]))
                    self.ui.Mplwidget.remove_car_from_map(tuple(event[0][1][1]))
                    self.control_events.remove(event)
                else:
                    self.control_events.remove(event)

        self.update_hospital_state(self.con.Hospitals)
        self.con.controllerMainLoop(self.tablica_komunikatow)
        self.update_widgets_scrol()

    def update_widgets_scrol(self):
        for elem in self.tablica_komunikatow:
            object = QLabel(elem)
            self.ui.verticalLayout_2.addWidget(object)
        self.tablica_komunikatow=[]

    def clear_widget_scrol(self):
        while self.ui.verticalLayout_2.count():
            item = self.ui.verticalLayout_2.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

    def update_hospital_state(self,hospitals):
        index=self.ui.hospwidget.glayout.count()
        for i in range(len(hospitals)):
            count_ambulances = np.in1d(hospitals[i].ambulances, 6).sum()
            self.ui.hospwidget.glayout.children()[i].itemAt(1).widget().setText(str(count_ambulances))
            self.ui.hospwidget.glayout.children()[i].itemAt(2).widget().changecolor(hospitals[i].personnel)
            self.ui.hospwidget.glayout.children()[i].itemAt(3).widget().changecolor(hospitals[i].volume)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


