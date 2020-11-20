import json

#Konwertowanie zdarzenia i paremtrów je opisujących do zwartej postacji JSON
#	event_name - nazwa zdarzenia w postaci napisu
#	paramList - LISTA! parametrów zdarzenia
def code_event(event_name, paramList):
	value = []
	for item in paramList:
		value.append(item)
	code = json.dumps({"name": event_name, "values": value})
	return code

#Dekodowanie zdarzenia
#Zwraca nazwę zdarzenia typu string oraz listę parametrów zdarzenia
def decode_event(sentence):
	event = json.loads(sentence)
	return event['name'], event['values']
