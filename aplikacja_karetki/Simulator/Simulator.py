from Simulator.Hospital import Hospital
from Simulator.Ambulance import Ambulance
from Simulator.Emergency import Emergency
from MessageController import MessageController
from Controller.ambulance_con import ambulanceState
from numpy import random
import numpy as np

class SimulatorSettings():
    def __init__(self):
        self.maxX = 600
        self.maxY = 550
        self.numberOfHospital = 10
        self.numberOfAmbulances = 50

class Simulator():
    def __init__(self, settings: SimulatorSettings, msgController: MessageController):
        self.__simulationSettings = settings
        self.__messageController = msgController
        self.__hospitalsList = []
        self.__ambulancesList = []
        self.__emergenciesMap = dict()
        self.__time = 0
        self.__timeToNewEmergency = 1
        self.__meanEmergency = 30
        self.__sigmaEmergency = 10
        self.__thresholdForEmergency = 20
        self.__meanAmbulanceServiceEme = 10
        self.__meanAmbulanceServiceHost = 10
        self.__meanAmbulanceQuarantine = 10
        self.__sigmaAmbulance = 15
        self.__meanTimeToEmptyBed = 150
        self.__sigmaTimeToEmptyBed = 20
        self.__minTreatmentTime = 7*24*60*60

        self.__hospitalsMap = dict()
        self.__emergenciesHosAmbMap = dict()

        '''
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

            self.__hospitalsList.append(Hospital((x, y)))
            self.__hospitalsMap[(x,y)] = len(self.__hospitalsList)-1
        '''
        # Wroclaw
        self.__hospitalsList.append(Hospital((165, 340)))
        self.__hospitalsMap[(165, 340)] = len(self.__hospitalsList) - 1
        # Poznan
        self.__hospitalsList.append(Hospital((162, 219)))
        self.__hospitalsMap[(162, 219)] = len(self.__hospitalsList) - 1
        # Rzeszow
        self.__hospitalsList.append(Hospital((467, 453)))
        self.__hospitalsMap[(467, 453)] = len(self.__hospitalsList) - 1
        # Warszawa
        self.__hospitalsList.append(Hospital((401, 234)))
        self.__hospitalsMap[(401, 234)] = len(self.__hospitalsList) - 1
        # Krakow
        self.__hospitalsList.append(Hospital((342, 439)))
        self.__hospitalsMap[(342, 439)] = len(self.__hospitalsList) - 1
        # Bialystok
        self.__hospitalsList.append(Hospital((522, 157)))
        self.__hospitalsMap[(522, 157)] = len(self.__hospitalsList) - 1
        # Szczecin
        self.__hospitalsList.append(Hospital((29, 125)))
        self.__hospitalsMap[(29, 125)] = len(self.__hospitalsList) - 1
        # Lublin
        self.__hospitalsList.append(Hospital((500, 325)))
        self.__hospitalsMap[(500, 325)] = len(self.__hospitalsList) - 1
        # Olsztyn
        self.__hospitalsList.append(Hospital((364, 99)))
        self.__hospitalsMap[(364, 99)] = len(self.__hospitalsList) - 1
        # Gdansk
        self.__hospitalsList.append(Hospital((261, 44)))
        self.__hospitalsMap[(261, 44)] = len(self.__hospitalsList) - 1

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
                

    def simulatorMianLoop(self,tablica_komunikatow,controlable_events):
        self.checkEmergencyTime(tablica_komunikatow)
        #for hospital in self.__hospitalsList:
        #    print(hospital.occupiedBeds)
        
        #print(self.__emergenciesHosAmbMap)
        # controlable_events.append(self.__messageController.readAllControllableEventsForSimulation())
        if self.__messageController.readAllControllableEventsForSimulation():
            controlable_events.append(self.__messageController.readAllControllableEventsForSimulation())
        # print(controlable_events)
        self.inputControllerEvents(tablica_komunikatow)
        self.updateState(tablica_komunikatow)
        self.__time += 1

    def checkEmergencyTime(self,tablica_komunikatow):
        if self.__time >= self.__timeToNewEmergency:
            self.__timeToNewEmergency = int(random.normal(self.__time + self.__meanEmergency, self.__sigmaEmergency))
            while self.__timeToNewEmergency <= self.__time:
                self.__timeToNewEmergency =int(random.normal(self.__time + self.__meanEmergency, self.__sigmaEmergency))


            #Zgloszenie w miejscu szpitalu jest dozwolone ????
            x = random.randint(0, self.__simulationSettings.maxX)
            y = random.randint(0, self.__simulationSettings.maxY)
            while (x, y) in self.__emergenciesMap:
                x = random.randint(0, self.__simulationSettings.maxX)
                y = random.randint(0, self.__simulationSettings.maxY)

            self.__emergenciesMap[(x, y)] = Emergency((x,y), self.__thresholdForEmergency)
            self.__messageController.addObservableEvent('E1o', [[x, y]])
            # print("New emergency, location: ", (x, y))
            tablica_komunikatow.append("E1o: New emergency, location:({},{})".format(x,y) )

    def inputControllerEvents(self,tablica_komunikatow):
        events = self.__messageController.readAllControllableEvents()
        for event in events:
            event_name = event[0]
            event_param = event[1]

            if event_name == 'E1c':
                startTime = self.__time

                distance = np.sqrt((self.__hospitalsList[event_param[0]-1].location[0]-event_param[2][0])**2 +
                                   (self.__hospitalsList[event_param[0]-1].location[1]-event_param[2][1])**2)
                finishTime = startTime + int(random.normal(distance, self.__sigmaAmbulance))
                while finishTime <= startTime:
                    finishTime = startTime + int(random.normal(distance, self.__sigmaAmbulance))

                self.__ambulancesList[event_param[1]-1].setAmbulanceState(ambulanceState.EMERGENCY_RIDE)
                self.__ambulancesList[event_param[1]-1].setAimLocation(event_param[2])
                self.__ambulancesList[event_param[1]-1].setStartTime(startTime)
                self.__ambulancesList[event_param[1]-1].setFinishTime(finishTime)

                self.__emergenciesMap[(event_param[2][0], event_param[2][1])].serviceEmergency()
                self.__emergenciesHosAmbMap[(event_param[2][0], event_param[2][1])] = [event_param[0]-1,event_param[1]-1]

                # print("An ambulance {} was sent from hospital {} to emergency in location {}".format(event_param[1],event_param[0], event_param[2]))
                tablica_komunikatow.append("E1c: An ambulance {} was sent from hospital {} to emergency in location {}".format(event_param[1],event_param[0], event_param[2]))
                                                                                    

                #print("Hospital {} location {}, ambulance {} start {}, finish {}, distance {}".format(event_param[0]-1,
                #        self.__hospitalsList[event_param[0]-1].location, event_param[1]-1,
                #        self.__ambulancesList[event_param[1]-1].getStartTime(),
                #        self.__ambulancesList[event_param[1]-1].getFinishTime(), distance))

            if event_name == 'E2c':
                [hospitalNumber, ambulanceNumber] = self.__emergenciesHosAmbMap[(event_param[1][0], event_param[1][1])]
                del self.__emergenciesHosAmbMap[(event_param[1][0], event_param[1][1])]
                del self.__emergenciesMap[(event_param[1][0], event_param[1][1])]

                startTime = self.__time

                distance = np.sqrt((self.__hospitalsList[event_param[0]-1].location[0]-event_param[1][0])**2 +
                                   (self.__hospitalsList[event_param[0]-1].location[1]-event_param[1][1])**2)
                finishTime = startTime + int(random.normal(distance, self.__sigmaAmbulance))
                while finishTime <= startTime:
                    finishTime = startTime + int(random.normal(distance, self.__sigmaAmbulance))

                self.__ambulancesList[ambulanceNumber].setAmbulanceState(ambulanceState.EMERGENCY_RIDE)
                self.__ambulancesList[ambulanceNumber].setAimLocation(self.__hospitalsList[event_param[0] - 1].location)
                self.__ambulancesList[ambulanceNumber].setStartTime(startTime)
                self.__ambulancesList[ambulanceNumber].setFinishTime(finishTime)

                self.__hospitalsList[event_param[0] - 1].newPatient(ambulanceNumber)
                self.__hospitalsList[event_param[0] - 1].removeAmbulanceWithList(ambulanceNumber)

                # print("Ambulance {} start return to hospital {}".format(ambulanceNumber + 1, event_param[0]))
                tablica_komunikatow.append("E2c: Ambulance {} started returning to hospital {}".format(ambulanceNumber + 1, event_param[0]))
                
                if self.__hospitalsList[event_param[0] - 1].occupiedBeds >= self.__hospitalsList[event_param[0] - 1].maxNumberOfBeds:
                    self.__messageController.addObservableEvent('E2o', [event_param[0]])
                    # print("Hospital {} is full".format(event_param[0]))
                    tablica_komunikatow.append("E2o: Hospital {} is full".format(event_param[0]))

            if event_name == 'E3c':
                startTime = self.__time
                locationHospital1 = self.__hospitalsList[event_param[0] - 1].location
                locationHospital2 = self.__hospitalsList[event_param[1] - 1].location

                distance = np.sqrt((locationHospital1[0] - locationHospital2[0]) ** 2 +
                                   (locationHospital1[1] - locationHospital2[1]) ** 2)

                finishTime = startTime + int(random.normal(distance, self.__sigmaAmbulance))
                while finishTime <= startTime:
                    finishTime = startTime + int(random.normal(distance, self.__sigmaAmbulance))

                self.__ambulancesList[event_param[2]-1].setAmbulanceState(ambulanceState.EMPTY_RIDE)
                self.__ambulancesList[event_param[2]-1].setAimLocation(self.__hospitalsList[event_param[1]-1].location)
                self.__ambulancesList[event_param[2]-1].setStartTime(startTime)
                self.__ambulancesList[event_param[2]-1].setFinishTime(finishTime)
                self.__hospitalsList[event_param[0]-1].removeAmbulanceWithList(event_param[2]-1)
                self.__hospitalsList[event_param[1]-1].addAmbulanceToList(event_param[2]-1)

                # print("Ambulance {} was sent from hospital {} to hospital {}".format(event_param[2] + 1, event_param[0] + 1, event_param[1] + 1))
                tablica_komunikatow.append("E3c: Ambulance {} was sent from hospital {} to hospital {}".format(event_param[2] + 1, event_param[0] + 1, event_param[1] + 1))
               

    def ambulancesDistribution(self):
    	dist = []
    	for hospital in self.__hospitalsList:
            dist.append(len(hospital.getAmbulancesList()))
    	return dist
    	
    def hospitalsLocations(self):
    	return np.array(list(self.__hospitalsMap.keys()))
    	
    def updateState(self,tablica_komunikatow):
        for i in range(len(self.__ambulancesList)):
            if self.__ambulancesList[i].getFinishTime() == self.__time:
                tempAmbulanceState = self.__ambulancesList[i].getAmbulanceState()

                if tempAmbulanceState == ambulanceState.EMERGENCY_RIDE:
                    ambulanceAim = tuple(self.__ambulancesList[i].getAimLocation())
                    if ambulanceAim in self.__emergenciesMap:

                        [hospitalNumber, ambulanceNumber] = self.__emergenciesHosAmbMap[ambulanceAim]
                        self.__messageController.addObservableEvent('E4o', [hospitalNumber+1, ambulanceNumber+1, ambulanceAim])

                        startTime = self.__time

                        finishTime = startTime + int(random.normal(self.__meanAmbulanceServiceEme, self.__sigmaAmbulance))
                        while finishTime <= startTime:
                            finishTime = startTime + int(random.normal(self.__meanAmbulanceServiceEme, self.__sigmaAmbulance))

                        self.__ambulancesList[i].setAmbulanceState(ambulanceState.PATIENT_SERVICE_AWAY)
                        self.__ambulancesList[i].setStartTime(startTime)
                        self.__ambulancesList[i].setFinishTime(finishTime)

                        # print("Ambulance {} start service emergence in place {}".format(i+1, ambulanceAim))
                        tablica_komunikatow.append("E4o: Ambulance {} started service in place {}".format(i+1, ambulanceAim))

                    elif self.__ambulancesList[i].getAimLocation() in self.__hospitalsMap:
                        hospitalNumber = self.__hospitalsMap[ambulanceAim]

                        self.__messageController.addObservableEvent('E6o', [hospitalNumber + 1, i + 1])

                        startTime = self.__time

                        finishTime = startTime + int(random.normal(self.__meanAmbulanceServiceHost, self.__sigmaAmbulance))
                        while finishTime <= startTime:
                            finishTime = startTime + int(random.normal(self.__meanAmbulanceServiceHost, self.__sigmaAmbulance))

                        self.__ambulancesList[i].setAmbulanceState(ambulanceState.PATIENT_SERVICE_HOSPITAL)
                        self.__ambulancesList[i].setStartTime(startTime)
                        self.__ambulancesList[i].setFinishTime(finishTime)

                        # print("Ambulance {} came back to hospital {}".format(i + 1, hospitalNumber+1))
                        tablica_komunikatow.append("E6o: Ambulance {} came back to hospital {} after emergency".format(i + 1, hospitalNumber+1))

                elif tempAmbulanceState == ambulanceState.PATIENT_SERVICE_AWAY:
                    emergenceLocation = tuple(self.__ambulancesList[i].getAimLocation())
                    emergence = self.__emergenciesMap[emergenceLocation]
                    [hospitalNumber, ambulanceNumber] = self.__emergenciesHosAmbMap[emergenceLocation]

                    if emergence.isNeedHospitalisation():
                        self.__messageController.addObservableEvent('E5o', [hospitalNumber + 1, i + 1, emergenceLocation])

                        self.__ambulancesList[i].setAmbulanceState(ambulanceState.EMERGENCY_RIDE)
                        self.__ambulancesList[i].setStartTime(0)
                        self.__ambulancesList[i].setFinishTime(0)

                        # print("Patient is ready to transport from {}".format(emergenceLocation))
                        tablica_komunikatow.append("E5o: Patient is ready to transport from {}".format(emergenceLocation))

                    else:
                        self.__messageController.addObservableEvent('E10o', [hospitalNumber + 1, i + 1, emergenceLocation])
                        del self.__emergenciesHosAmbMap[emergenceLocation]
                        del self.__emergenciesMap[emergenceLocation]

                        startTime = self.__time

                        distance = np.sqrt(
                            (self.__hospitalsList[hospitalNumber].location[0] - emergenceLocation[0]) ** 2 +
                            (self.__hospitalsList[hospitalNumber].location[1] - emergenceLocation[1]) ** 2)
                        finishTime = startTime + int(random.normal(distance, self.__sigmaAmbulance))
                        while finishTime <= startTime:
                            finishTime = startTime + int(random.normal(distance, self.__sigmaAmbulance))

                        self.__ambulancesList[i].setAmbulanceState(ambulanceState.EMPTY_RIDE)
                        self.__ambulancesList[i].setAimLocation(self.__hospitalsList[hospitalNumber].location)
                        self.__ambulancesList[i].setStartTime(startTime)
                        self.__ambulancesList[i].setFinishTime(finishTime)

                        # print("Ambulance {} is coming back to hospital {} after service emergence".format(i+1, hospitalNumber + 1))
                        tablica_komunikatow.append("E10o: Ambulance {} came back to hospital {} after service emergence".format(i+1, hospitalNumber + 1))

                elif tempAmbulanceState == ambulanceState.PATIENT_SERVICE_HOSPITAL:
                    hospitalNumber = self.__hospitalsMap[tuple(self.__ambulancesList[i].getAimLocation())]
                    self.__messageController.addObservableEvent('E7o', [hospitalNumber + 1, i + 1])

                    startTime = self.__time

                    finishTime = startTime + int(random.normal(self.__meanAmbulanceQuarantine, self.__sigmaAmbulance))
                    while finishTime <= startTime:
                        finishTime = startTime + int(
                            random.normal(self.__meanAmbulanceQuarantine, self.__sigmaAmbulance))

                    self.__ambulancesList[i].setAmbulanceState(ambulanceState.QUARANTINE)
                    self.__ambulancesList[i].setAimLocation(self.__hospitalsList[hospitalNumber].location)
                    self.__ambulancesList[i].setStartTime(startTime)
                    self.__ambulancesList[i].setFinishTime(finishTime)

                    self.__hospitalsList[hospitalNumber].finishPatientService()

                    if(self.__hospitalsList[hospitalNumber].timeToEmptyBed < self.__time):

                        finishTime = startTime + int(
                            random.normal(self.__meanTimeToEmptyBed, self.__sigmaTimeToEmptyBed)) + self.__minTreatmentTime
                        while finishTime <= startTime:
                            finishTime = startTime + int(
                                random.normal(self.__meanTimeToEmptyBed, self.__sigmaTimeToEmptyBed))

                        self.__hospitalsList[hospitalNumber].timeToEmptyBed = finishTime

                    # print("Ambulance {} start quarantine in hospital {}".format(i + 1, hospitalNumber + 1))
                    tablica_komunikatow.append("E7o: Ambulance {} start quarantine in hospital {}".format(i + 1, hospitalNumber + 1))

                elif tempAmbulanceState == ambulanceState.QUARANTINE:
                    hospitalNumber = self.__hospitalsMap[tuple(self.__ambulancesList[i].getAimLocation())]
                    self.__messageController.addObservableEvent('E8o', [hospitalNumber + 1, i + 1])

                    self.__ambulancesList[i].setAmbulanceState(ambulanceState.READY)
                    self.__ambulancesList[i].setAimLocation(self.__hospitalsList[hospitalNumber].location)
                    self.__ambulancesList[i].setStartTime(0)
                    self.__ambulancesList[i].setFinishTime(0)

                    # print("Ambulance {} finished quarantine in hospital {}".format(i + 1, hospitalNumber + 1))
                    tablica_komunikatow.append("E8o: Ambulance {} finished quarantine in hospital {}".format(i + 1, hospitalNumber + 1))

                elif tempAmbulanceState == ambulanceState.EMPTY_RIDE:
                    hospitalNumber = self.__hospitalsMap[tuple(self.__ambulancesList[i].getAimLocation())]
                    self.__messageController.addObservableEvent('E9o', [hospitalNumber + 1, i + 1])

                    self.__ambulancesList[i].setAmbulanceState(ambulanceState.READY)
                    self.__ambulancesList[i].setAimLocation(self.__hospitalsList[hospitalNumber].location)
                    self.__ambulancesList[i].setStartTime(0)
                    self.__ambulancesList[i].setFinishTime(0)

                    # print("Ambulance {} finished ride to hospital {}".format(i + 1, hospitalNumber + 1))
                    tablica_komunikatow.append("E9o: Ambulance {} finished ride to hospital {}".format(i + 1, hospitalNumber + 1))

        for i in range(len(self.__hospitalsList)):
            if self.__hospitalsList[i].timeToEmptyBed == self.__time:
                if self.__hospitalsList[i].occupiedBeds > 0:

                    if self.__hospitalsList[i].occupiedBeds == self.__hospitalsList[i].maxNumberOfBeds:
                        self.__messageController.addObservableEvent('E3o', [i + 1])

                    self.__hospitalsList[i].occupiedBeds -= 1

                    if self.__hospitalsList[i].occupiedBeds > 0:
                        startTime = self.__time

                        finishTime = startTime + int(
                            random.normal(self.__meanTimeToEmptyBed, self.__sigmaTimeToEmptyBed))
                        while finishTime <= startTime:
                            finishTime = startTime + int(
                                random.normal(self.__meanTimeToEmptyBed, self.__sigmaTimeToEmptyBed))

                        self.__hospitalsList[i].timeToEmptyBed = finishTime

                    # print("Patient recovered in hospital {}".format(i+1))
                    tablica_komunikatow.append("E3o: Patient recovered in hospital {}".format(i+1))
