from event import Event

class EventList:
    sorted = False
    events = list()
    ignoredEvents = set()

    def __iter__(self):
        return iter(self.events)

    def append(self, x):
        if not hash(x) in self.ignoredEvents:
            self.events.append(x)
            self.ignoredEvents.add(hash(x))

    def hasEvent(self, x):
        return x in self.events

    def sortList(self):
        self.events = sorted(self.events, key=lambda Event : Event.epoch)