class EventSystem:
    def __init__(self):
        self.listeners = {}

    def add_listener(self, event_type, callback):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def remove_listener(self, event_type, callback):
        if event_type in self.listeners:
            self.listeners[event_type].remove(callback)

    def dispatch_event(self, event_type, *args, **kwargs):
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                callback(*args, **kwargs)