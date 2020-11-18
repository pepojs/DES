from Hospital import Hospital
from Ambulance import Ambulance
import Emergency
from numpy import random

class SimulatorSettings():
    def __init__(self):
        self.maxX = 100
        self.maxY = 100
        self.numberOfHospital = 10
        self.numberOfAmbulances = 50

class Simulator():
    def __init__(self, settings: SimulatorSettings):
        self.__hospitalsList = []
        self.__ambulancesList = []
        self.__emergenciesList = []
        self.__time = 0
        self.__timeToNewEmergency = 1

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
