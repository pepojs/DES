from Simulator.Simulator import Simulator, SimulatorSettings
from MessageController import MessageController
def main():
    messageController = MessageController()

    simSettings = SimulatorSettings()
    sim = Simulator(simSettings, messageController)
    for i in range(100):
        sim.simulatorMianLoop()

    events = messageController.readAllObservableEvents()
    messageController.addControllableEvents('E1c', [0,0,[events[0][1][0], events[0][1][1]]])
    sim.simulatorMianLoop()

if __name__ == '__main__':
    main()