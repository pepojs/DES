import json

class MessageController():
    def __init__(self):
        self.__observableEventsBuffer = []
        self.__controllableEventsBuffer = []

    def addObservableEvent(self, name, paramList):
        code = self.code_event(name, paramList)
        self.__observableEventsBuffer.append(code)

    def addControllableEvents(self, name, paramList):
        code = self.code_event(name, paramList)
        self.__controllableEventsBuffer.append(code)

    def readAllObservableEvents(self):
        events = []
        for i in self.__observableEventsBuffer:
            events.append(self.decode_event(i))
        self.__observableEventsBuffer.clear()
        return events

    def readAllControllableEvents(self):
        events = []
        for i in self.__controllableEventsBuffer:
            events.append(self.decode_event(i))
        self.__controllableEventsBuffer.clear()
        return events

    # Konwertowanie zdarzenia i paremtrów je opisujących do zwartej postacji JSON
    #	event_name - nazwa zdarzenia w postaci napisu
    #	paramList - LISTA! parametrów zdarzenia
    def code_event(self, event_name, paramList):
        value = []
        for item in paramList:
            value.append(item)
        code = json.dumps({"name": event_name, "values": value})
        return code

    # Dekodowanie zdarzenia
    # Zwraca nazwę zdarzenia typu string oraz listę parametrów zdarzenia
    def decode_event(self, sentence):
        event = json.loads(sentence)
        return event['name'], event['values']
