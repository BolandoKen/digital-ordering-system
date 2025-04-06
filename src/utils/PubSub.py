
class Pubsub(object) :
    def __init__(self):
        self.events = {}

    def sub(self, eventName, callback) :
        if eventName not in self.events : 
            self.events[eventName] = [callback]
        else :
            self.events[eventName].append(callback)

    def pub(self, eventName, params) :
        if eventName in self.events :
            for callback in self.events[eventName] :
                callback(params)
        else :
            print("error: no subscribers for", eventName)

pubsub = Pubsub()
