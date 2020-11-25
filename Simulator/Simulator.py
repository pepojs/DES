from Simulator.Hospital import Hospital
from Simulator.Ambulance import Ambulance
from Simulator.Emergency import Emergency
from MessageController import MessageController
from Controller.ambulance_con import ambulanceState
from numpy import random
import numpy as np

class SimulatorSettings():
    def __init__(self):
        self.maxX = 100
        self.maxY = 100
        self.numberOfHospital = 10
        self.numberOfAmbulances = 50

class Simulator():
    def __init__(self, settings: SimulatorSettings, msgController: MessageController):
        self.__simulationSettings = settings
        self.__messageController = msgController
        self.__hospitalsList = []
        self.__ambulancesList = []
        self.__emergenciesList = []
        self.__time = 0
        self.__timeToNewEmergency = 1
        self.__meanEmergency = 15
        self.__sigmaEmergency = 5
        self.__thresholdForEmergency = 20
        self.__sigmaAmbulance = 15
        self.__emergenciesMap = dict()
        self.__hospitalsMap = dict()

        assert(settings.maxX * settings.maxY >= settings.numberOfHospital), "Map is too small !!!"

        tempLockedX = [0] * (settings.maxX + 1)
        tempLockedY = [0] * (settings.maxY + 1)

        for i in range(settings.numberOfHospital):
            x = random.randint(0, settings.maxX)
            while tempLockedX[x] != 0:
                x = random.randint(0, settings.maxX)

            tempLockedX[x] = 1

            y = random.randint(0, settings.maxY)
            while tempLockedY[y] != 0:
                y = random.randint(0, settings.maxY)

            tempLockedY[y] = 1

            self.__hospitalsList.append(Hospital((x,y)))

        for i in range(settings.numberOfAmbulances):
            self.__ambulancesList.append(Ambulance())

        ambulancesInHospital = [0] * settings.numberOfHospital
        ambulancesAssing = False

        mean = int(settings.numberOfAmbulances/settings.numberOfHospital)
        sigma = (mean - 1)/3

        while ambulancesAssing != True:
            assingedAmbulances = 0

            for i in range(settings.numberOfHospital - 1):
                radomNumber = int(random.normal(mean, sigma))
                ambulancesInHospital[i] = radomNumber
                assingedAmbulances += radomNumber

            if assingedAmbulances <= settings.numberOfAmbulances - (mean - 3*sigma):
                ambulancesInHospital[settings.numberOfHospital - 1] = settings.numberOfAmbulances - assingedAmbulances
                ambulancesAssing = True

        temp = 0
        for i in range(settings.numberOfHospital):
            for j in range(ambulancesInHospital[i]):
                self.__hospitalsList[i].addAmbulanceToList(temp)
                temp += 1

    def simulatorMianLoop(self):
        self.checkEmergencyTime()
        self.inputControllerEvents()
        self.updateState()
        self.__time += 1

    def checkEmergencyTime(self):
        if self.__time >= self.__timeToNewEmergency:
            self.__timeToNewEmergency = int(random.normal(self.__time + self.__meanEmergency, self.__sigmaEmergency))
            while self.__timeToNewEmergency <= self.__time:
                self.__timeToNewEmergency =int(random.normal(self.__time + self.__meanEmergency, self.__sigmaEmergency))


            #Zgloszenie w miejscu szpitalu jest dozwolone ????
            x = random.randint(0, self.__simulationSettings.maxX)
            y = random.randint(0, self.__simulationSettings.maxY)

            self.__emergenciesList.append(Emergency((x,y), self.__thresholdForEmergency))
            self.__emergenciesMap[(x,y)] = len(self.__emergenciesList) - 1
            self.__messageController.addObservableEvent('E1o', [x, y])
            print(self.__emergenciesMap)

    def inputControllerEvents(self):
        events = self.__messageController.readAllControllableEvents()
        for event in events:
            if event[0] == 'E1c':
                startTime = self.__time

                distance = np.sqrt(np.sum((self.__hospitalsList[event[1][0]-1].location-event[1][2])**2))
                finishTime = startTime + int(random.normal(distance, self.__sigmaAmbulance))
                while finishTime <= startTime:
                    finishTime = startTime + int(random.normal(distance, self.__sigmaAmbulance))

                self.__ambulancesList[event[1][1]].setAmbulanceState(ambulanceState.EMERGENCY_RIDE)
                self.__ambulancesList[event[1][1]].setAimLocation(event[1][2])
                self.__ambulancesList[event[1][1]].setStartTime(startTime)
                self.__ambulancesList[event[1][1]].setFinishTime(finishTime)

                emergencyNumber = self.__emergenciesMap[event[1][2]]
                print(emergencyNumber)
                self.__emergenciesList[emergencyNumber].serviceEmergency()

    def updateState(self):
        pass

    def InputControllerEvents(self):
        pass

    def sendNewEvent(self, name, values):
        pass