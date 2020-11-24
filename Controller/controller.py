import numpy as np
from ambulance_con import ambulanceState
import hospital_con as hosp
import sys
from events_coding import *
import random

class Controller:
	#Dane wejściowe do sterownika - liczba szpitali n i ich położenie locations, liczba karetek m, ograniczenia ze względu na rozmiar mapy xmax, ymax. 
	#Liczba karetek zadawana w formie wektora Numpy.
	#Można zadać odmienną liczbę karetek dla każdego szpitala lub podać jedną wartość - tyle samo karetek w każdym szpitalu
	def __init__(self,n,m,locations,xmax,ymax):
		self.Xmax = xmax
		self.Ymax = ymax
		self.Hospitals = []
		self.ambulanceMatrix = self.createAmbulanceMatrix(n,m)
		#self.eventList = []
		for i in range(n):
			self.Hospitals.append(hosp.hospital_con(locations[i],self.ambulanceMatrix[i]))
		
		
	
	def createAmbulanceMatrix(self,n,m):
		if len(m)==1:
			A = np.zeros((n,n*sum(m)))
			for i in range(n):
				for j in range(i*m[0],(i+1)*m[0]):
					A[i][j] = ambulanceState.READY.value
		elif len(m)>1:
			A = np.zeros((n,sum(m)))
			for i in range(n):
				for j in range(sum(m[:i]),sum(m[:(i+1)])):
					A[i][j] = ambulanceState.READY.value
		return A
	
	def printState (self):
		ambulance_state = []
		for i in range(len(self.Hospitals)):
			print("Hospital ",i+1)
			print("Location:       ", self.Hospitals[i].location)
			print("Free places:    ", self.Hospitals[i].volume)
			print("Free personnel: ", self.Hospitals[i].personnel)
			for k in self.Hospitals[i].ambulances:
				if k==0:
					ambulance_state.append(0)
				else:
					ambulance_state.append(ambulanceState(k).name)
			print("Ambulances: ")
			print(ambulance_state)
			print("################")
			ambulance_state.clear()
		print('Lists of awaiting events:')
		#for item in self.eventList:
		#	print(item)
	
	#Odbieranie zdarzeń obserwowalnych
	#Funkcja rozpoznaję nazwę zdarzenia i sprawdza, czy zdefiniowano odpowiednią liczbę parametrów
	#Ponadto sprawdzane są warunki dopuszczalności zdarzeń
	#Komendy typu 'finish_ij' należy przekazywać jako dwie osobne liczby i, j
	def observableEvents(self,coded_event):
		event, value = decode_event(coded_event)
		if event=='E1o':
			if len(value)==1: #weryfikacja definicji
				if value[0][0]>=0 or value[0][0]<=self.Xmax or value[0][1]>=0 or value[0][1]<=self.Ymax: #warunek dopuszczalności  
					print(self.generateE1c(value[0]))
					return True
				print('Otrzymane zdarzenie E1o jest niedopuszczalne!')
				return False
			print('Błędna definicja zdarzenia E1o')
			return False
		elif event=='E2o':
			if len(value)==1:
				if  self.Hospitals[value[0]-1].volume == True: #warunek dopuszczalności 
					self.Hospitals[value[0]-1].volume = False
					return True
				print('Otrzymane zdarzenie E2o jest niedopuszczalne')
				return False
			print('Błędna definicja zdarzenia E2o')
			return False
		elif event=='E3o':
			if len(value)==1:
				if  self.Hospitals[value[0]-1].volume == False: #warunek dopuszczalności 
					self.Hospitals[value[0]-1].volume = True
					return True
				print('Otrzymane zdarzenie E3o jest niedopuszczalne')
				return False
			print('Błędna definicja zdarzenia E3o')
			return False
		elif event=='E4o':
			if len(value)==3:
				if  self.Hospitals[value[0]-1].ambulances[value[1]-1] == ambulanceState.EMERGENCY_RIDE.value: #warunek dopuszczalności 
					self.Hospitals[value[0]-1].ambulances[value[1]-1] = ambulanceState.PATIENT_SERVICE_AWAY.value
					return True
				print('Otrzymane zdarzenie E4o jest niedopuszczalne')
				return False
			print('Błędna definicja zdarzenia E4o')
			return False
		elif event=='E5o':
			if len(value)==3:
				if  self.Hospitals[value[0]-1].ambulances[value[1]-1] == ambulanceState.PATIENT_SERVICE_AWAY.value: #warunek dopuszczalności 
					print(self.generateE2c(value[0],value[1],value[2]))
					return True
				print('Otrzymane zdarzenie E5o jest niedopuszczalne')
				return False
			print('Błędna definicja zdarzenia E5o')
			return False
		elif event=='E6o':
			if len(value)==2:
				if  self.Hospitals[value[0]-1].ambulances[value[1]-1] == ambulanceState.EMERGENCY_RIDE.value: #warunek dopuszczalności 
					self.Hospitals[value[0]-1].ambulances[value[1]-1] = ambulanceState.PATIENT_SERVICE_HOSPITAL.value
					return True
				print('Otrzymane zdarzenie E6o jest niedopuszczalne')
				return False
			print('Błędna definicja zdarzenia E6o')
			return False
		elif event=='E7o':
			if len(value)==2:
				if  self.Hospitals[value[0]-1].ambulances[value[1]-1] == ambulanceState.PATIENT_SERVICE_HOSPITAL.value: #warunek dopuszczalności 
					self.Hospitals[value[0]-1].ambulances[value[1]-1] = ambulanceState.QUARANTINE.value
					self.Hospitals[value[0]-1].personnel = True
					return True
				print('Otrzymane zdarzenie E7o jest niedopuszczalne')
				return False
			print('Błędna definicja zdarzenia E7o')
			return False
		elif event=='E8o':
			if len(value)==2:
				if self.Hospitals[value[0]-1].ambulances[value[1]-1] == ambulanceState.QUARANTINE.value: #warunek dopuszczalności 
					self.Hospitals[value[0]-1].ambulances[value[1]-1] = ambulanceState.READY.value
					return True
				print('Otrzymane zdarzenie E8o jest niedopuszczalne')
				return False
			print('Błędna definicja zdarzenia E8o')
			return False
		elif event=='E9o':
			if len(value)==2:
				if  self.Hospitals[value[0]-1].ambulances[value[1]-1] == ambulanceState.EMPTY_RIDE.value: #warunek dopuszczalności 
					self.Hospitals[value[0]-1].ambulances[value[1]-1] = ambulanceState.READY.value
					return True
				print('Otrzymane zdarzenie E9o jest niedopuszczalne')
				return False
			print('Błędna definicja zdarzenia E9o')
			return False
		elif event=='E10o':
			if len(value)==2:
				if  self.Hospitals[value[0]-1].ambulances[value[1]-1] == ambulanceState.PATIENT_SERVICE_AWAY.value: #warunek dopuszczalności 
					self.Hospitals[value[0]-1].ambulances[value[1]-1] = ambulanceState.EMPTY_RIDE.value
					return True
				print('Otrzymane zdarzenie E10o jest niedopuszczalne')
				return False
			print('Błędna definicja zdarzenia E10o')
			return False
			
		print('Nie zdefiniowano takiego zdarzenia obserwowalnego')
		return False
		
	#Generuje zdarzenie kontrolowalne nr 1
	def generateE1c (self,location):
		i,j = self.chooseHospital(location) #weryfikuje warunek dopuszczalności
		if i > -1 and j > -1:
			self.Hospitals[i-1].ambulances[j-1] = ambulanceState.EMERGENCY_RIDE.value
			return code_event('E1c',[i,j,location])
		
	#Funkcja znajduje szpital znajdujący się najbliżej zgłoszonego miejsca zdarzenia
	#Ze szpitala losowo wybierana jest dostępna karetka, która podejmuje akcje
	#Jeśli nie zostanie znaleziony szpital, który może zrealizować zadanie, zwracane są wartości (-1, -1)
	def chooseHospital(self,Lp):
		dist = np.Inf
		i = -1
		j = -1
		for iter in range(len(self.Hospitals)):
			tmp_dist = np.sqrt(np.sum((self.Hospitals[iter].location-Lp)**2))
			amb = np.where(self.Hospitals[iter].ambulances == ambulanceState.READY.value)[0].tolist()
			if len(amb)>0:
				if tmp_dist < dist:
					i = iter+1
					j = amb[random.randint(0,len(amb)-1)]
					dist = tmp_dist
		return i,j
	
	#Generuje zdarzenie E2c
	def generateE2c (self,l,j,location):
		i = self.findHospital(location) #weryfikuje warunek dopuszczalności
		if i > -1:
			self.Hospitals[i-1].personnel = False
			self.Hospitals[i-1].ambulances[j-1] = ambulanceState.EMERGENCY_RIDE.value
			if l!=i:
				self.Hospitals[l-1].ambulances[j-1] = 0
			return code_event('E2c',[i,location])
	
	#Funkcja znajduje szpital najbliżej miejsca zgłoszenia, który może aktualnie przyjąć chorego
	def findHospital(self,Lp):
		dist = np.Inf
		i = -1
		for iter in range(len(self.Hospitals)):
			if self.Hospitals[iter].volume and self.Hospitals[iter].personnel:
				tmp_dist = np.sqrt(np.sum((self.Hospitals[iter].location-Lp)**2))
				if tmp_dist < dist:
					i = iter+1
					dist = tmp_dist
		return i
			
				
		
		
				

#Próba wypisania aktualnego stanu i reakcji na zdarzenia
n=5
m=[7]
xmax = 100
ymax = 100
locations = np.random.rand(n,2)*[xmax,ymax]
con = Controller(n,np.array(m),locations,xmax,ymax)
con.printState()

#Test działają dla karetki nr 19 ze szpitala nr 3
zgloszenie = [locations[2][0]-5, locations[2][1]-4]
print('\n\n')
event = code_event('E1o', [zgloszenie])
print('EVENT!!!!!!!!!!!!!!!!!!!')
print(event)
if con.observableEvents(event):
	con.printState()
print('\n\n')
event = code_event('E2o', [4])
print('EVENT!!!!!!!!!!!!!!!!!!!')
print(event)
if con.observableEvents(event):
	con.printState()
print('\n\n')
event = code_event('E3o', [4])
print('EVENT!!!!!!!!!!!!!!!!!!!')
print(event)
if con.observableEvents(event):
	con.printState()
print('\n\n')
event = code_event('E4o', [3,19,zgloszenie])
print('EVENT!!!!!!!!!!!!!!!!!!!')
print(event)
if con.observableEvents(event):
	con.printState()
print('\n\n')
event = code_event('E5o', [3,19,zgloszenie])
print('EVENT!!!!!!!!!!!!!!!!!!!')
print(event)
if con.observableEvents(event):
	con.printState()
print('\n\n')
event = code_event('E6o', [3,19])
print('EVENT!!!!!!!!!!!!!!!!!!!')
print(event)
if con.observableEvents(event):
	con.printState()
print('\n\n')
event = code_event('E7o', [3,19])
print('EVENT!!!!!!!!!!!!!!!!!!!')
print(event)
if con.observableEvents(event):
	con.printState()
print('\n\n')
event = code_event('E8o', [3,19])
print('EVENT!!!!!!!!!!!!!!!!!!!')
print(event)
if con.observableEvents(event):
	con.printState()
print('\n\n')
event = code_event('E1o', [zgloszenie])
print('EVENT!!!!!!!!!!!!!!!!!!!')
print(event)
if con.observableEvents(event):
	con.printState()
print('\n\n')
event = code_event('E4o', [3,19,zgloszenie])
print('EVENT!!!!!!!!!!!!!!!!!!!')
print(event)
if con.observableEvents(event):
	con.printState()
print('\n\n')
event = code_event('E10o', [3,19])
print('EVENT!!!!!!!!!!!!!!!!!!!')
if con.observableEvents(event):
	con.printState()
print('\n\n')
event = code_event('E9o', [3,19])
print('EVENT!!!!!!!!!!!!!!!!!!!')
if con.observableEvents(event):
	con.printState()
print('\n\n')
