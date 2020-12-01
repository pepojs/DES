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
			amb = self.chooseFreeAmbulance(self.Hospitals[iter],1)
			if amb>-1:
				if tmp_dist < dist:
					i = iter+1
					j = amb+1
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
		
	#Zdarzenie może nie zostać wywołane - nałożony dodatkowy warunek dopuszczalności, że szpitale i,j muszą być dostatecznie blisko siebie
	def generateE3c(self,i,j,k):
		self.Hospitals[i-1].ambulances[k-1] = 0
		self.Hospitals[j-1].ambulances[k-1] = ambulanceState.EMPTY_RIDE.value
		return code_event('E3c',[i,j,k])
	
	#Sprawdza, w których szpitalach nie ma dostępnych ambulansów
	#Jeśli do szpitala zmierza ambulans z pustym przejazdem, to taki szpital również jest pomijany
	def lackOfAmbulances(self):
		emptyHospitals = []
		for idx in range(len(self.Hospitals)):
			i = 0
			length = len(self.Hospitals[idx].ambulances)
			while i<length:
				if self.Hospitals[idx].ambulances[i] == ambulanceState.READY.value or self.Hospitals[idx].ambulances[i] == ambulanceState.EMPTY_RIDE.value:
					break
				i = i+1
			if i==length:
				emptyHospitals.append(idx+1)		
		return emptyHospitals
	
	#Funkcja weryfikuje, w których szpitalach nie ma gotowych karetek
	#Następnie, dla każdego znalezionego szpitala znajduje szpitale, które znajdują się dostatecznie blisko
	#Spośród tych szpitali wybiera najbliższy, w którym dostępne są co najmniej 3 karetki
	#Jeśli znajdzie taki szpital, to generuje zdarzenie kontrolowalne E3c
	#	radius - promień poszukiwań pobliskiego szpitala
	#	minAmbulances - minimalna liczba karetek w pobliskim szpitalu, aby móc prosić go o pomoc
	def ambulanceArrangementCheck(self,radius,minAmbulances):
		emptyHospitals = self.lackOfAmbulances()
		if len(emptyHospitals)>0:
			for j in emptyHospitals:
				close,dist = self.nearHospital(j-1,radius)
				itr = 0
				length = len(close)
				while itr < length:
					ind = dist.index(min(dist))
					dist.pop(ind)
					i = close[ind]
					close.pop(ind)
					k = self.chooseFreeAmbulance(self.Hospitals[i-1],minAmbulances)
					if k > -1: #warunek dopuszczalności
						print(self.generateE3c(i,j,k+1))
						break
					itr = itr + 1
	
	#Znajduje szpitale bliskie wskazanemu szpitalu. Szpitale muszą się znajdować odpowiednio blisko.
	#	hospital - indeks szpitala, do którego poszukujemy bliskich szpitali
	#	radius - promień obszaru, w którym szukamy szpitala
	def nearHospital(self,hospital,radius):
		min_dist = abs(max(self.Xmax*radius,self.Ymax*radius))
		close = []
		dist = []
		for iter in range(len(self.Hospitals)):
			if iter != hospital-1:
				tmp_dist = np.sqrt(np.sum((self.Hospitals[iter].location-self.Hospitals[hospital].location)**2))
				if tmp_dist > 0 and tmp_dist <= min_dist:
					close.append(iter+1)
					dist.append(tmp_dist)
		return close,dist
		
	#Funkcja losująca ambulans ze wszystkich dostępnych w danym szpitalu.
	#Jeśli nie ma takiego ambulansu, to funkcja zwraca -1.
	#	hospital - szpital, z którego wybierany ambulans
	#	minAmbulances - minimalna liczba karetek, która musi znajdować się w szpitalu przed wylosowaniem
	def chooseFreeAmbulance(self,hospital,minAmbulances):
		amb = np.where(hospital.ambulances == ambulanceState.READY.value)[0].tolist()
		if len(amb)>=minAmbulances:
			j = amb[random.randint(0,len(amb)-1)]
			return j
		return -1
			
				

#Próba wypisania aktualnego stanu i reakcji na zdarzenia
n=5
m=[7]
#m=[5,4,0,2,0] #Do weryfikacji zdarzenia E3c
xmax = 100
ymax = 100
locations = np.random.rand(n,2)*[xmax,ymax]
con = Controller(n,np.array(m),locations,xmax,ymax)

con.printState()
#print('\n')
#print('E3c - TESTY')
#print('############E3c############')
#con.ambulanceArrangementCheck(0.7,3)
#con.printState()
#print('\n')
#con.ambulanceArrangementCheck(0.7,3)
#con.printState()
#print('############E3c############')
#print('\n')

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
print(event)
if con.observableEvents(event):
	con.printState()
print('\n\n')
event = code_event('E9o', [3,19])
print('EVENT!!!!!!!!!!!!!!!!!!!')
print(event)
if con.observableEvents(event):
	con.printState()
print('\n\n')
