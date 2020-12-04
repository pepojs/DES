from Simulator.Simulator import Simulator, SimulatorSettings
from MessageController import MessageController
def main():
    messageController = MessageController()

    simSettings = SimulatorSettings()
    sim = Simulator(simSettings, messageController)
    for i in range(100):
        sim.simulatorMianLoop()

    events = messageController.readAllObservableEvents()
    messageController.addControllableEvents('E1c', [1, 1, [events[0][1][0], events[0][1][1]]])

    for i in range(1000):
        sim.simulatorMianLoop()

    messageController.addControllableEvents('E2c', [3, [events[0][1][0], events[0][1][1]]])

    for i in range(100):
        sim.simulatorMianLoop()

if __name__ == '__main__':
    main()