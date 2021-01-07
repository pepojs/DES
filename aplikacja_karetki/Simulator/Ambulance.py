from enum import Enum
from Controller.ambulance_con import ambulanceState

class Ambulance():
    def __init__(self):
        self.__state = ambulanceState.READY
        self.__aimLocation = (0,0)
        self.__startTime = 0
        self.__finishTime = 0

    def setAmbulanceState(self, newState: ambulanceState):
        self.__state = newState

    def setAimLocation(self, newAim):
        self.__aimLocation = newAim

    def setStartTime(self, newStartTime):
        self.__startTime = newStartTime

    def setFinishTime(self, newFinishTime):
        self.__finishTime = newFinishTime

    def getAmbulanceState(self):
        return self.__state

    def getAimLocation(self):
        return self.__aimLocation

    def getStartTime(self):
        return self.__startTime

    def getFinishTime(self):
        return self.__finishTime