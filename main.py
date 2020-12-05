from Controller.controller import Controller
from Simulator.Simulator import Simulator, SimulatorSettings
from MessageController import MessageController
def main():
	messageController = MessageController()

	simSettings = SimulatorSettings()
	sim = Simulator(simSettings, messageController)
	
	con = Controller(simSettings, sim.hospitalsLocations(), messageController)
	con.printState()
    
	for i in range(1000):
        	sim.simulatorMianLoop()
        	con.controllerMainLoop()
        	i = input()
        	if i=='y': #write y to show the current state
        		con.printState()
        	#writ anything else to continue

if __name__ == '__main__':
	main()
