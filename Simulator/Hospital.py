from numpy import random

class Hospital():
    def __init__(self, location):
        self.location = location
        self.maxNumberOfBeds = random.randint(100, 200)
        self.occupiedBeds = 0
        self.personnelAreAvailable = True
        self.__ambulanceList = []
        self.timeToEmptyBed = 0

    def newPatient(self, ambulanceNumber):
        if self.occupiedBeds < self.maxNumberOfBeds:
            self.occupiedBeds = self.occupiedBeds + 1
            self.personnelAreAvailable = False
            self.ambulanceList.append(len(self.ambulanceList), ambulanceNumber)
            return True
        else:
            return False

    def isEmptyBed(self):
        if self.occupiedBeds < self.maxNumberOfBeds:
            return True
        else:
            return False

    def removeAmbulanceWithList(self, ambulanceNumber):
        self.__ambulanceList.remove(ambulanceNumber)

    def finishPatientService(self):
        self.personnelAreAvailable = True

    def addAmbulanceToList(self, ambulanceNumber):
        self.__ambulanceList.append(ambulanceNumber)

    def getAmbulancesList(self):
        return self.__ambulanceList


