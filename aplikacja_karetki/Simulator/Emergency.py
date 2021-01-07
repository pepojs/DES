from numpy import random

class Emergency():
    def __init__(self, location, threshold):
        self.location = location
        self.service = False

        r = random.randint(0, 100)
        if r >= threshold:
            self.needHospitalisation = True
        else:
            self.needHospitalisation = False

    def getLocation(self):
        return self.location

    def serviceEmergency(self):
        self.service = True

    def isService(self):
        return self.service

    def isNeedHospitalisation(self):
        return self.needHospitalisation