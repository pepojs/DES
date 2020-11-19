import numpy as np
from ambulance_con import ambulanceState
import hospital_con as hosp
import sys

class Controller:
	#Dane wejściowe do sterownika - liczba szpitali i ich położenie, liczba karetek. 
	#Liczba karetek zadawana w formie wektora Numpy.
	#Można zadać odmienną liczbę karetek dla każdego szpitala lub podać jedną wartość - tyle samo karetek w każdym szpitalu
	def __init__(self,n,m,locations):
		self.Hospitals = []
		self.ambulanceMatrix = self.createAmbulanceMatrix(n,m)
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
		

#Próba wypisania aktualnego stanu
n=5
m=[7]
xmax = 100
ymax = 100
locations = np.random.rand(n,2)*[xmax,ymax]
con = Controller(n,np.array(m),locations)
con.printState()
