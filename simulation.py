from Queue import Queue


class Simulation:

    queue = Queue()
    current_time = 0

    def __init__(self):
        pass

    def schedule_event(self, event):
        event_type, scheduled_time, _ = event

        self.queue.put(event)

    def advance_time(self):
        """

        :return:
        """
        events_happened = []
        while not self.queue.empty():
            next_event = self.queue.get()
            events_happened.extend(next_event)
            self.current_time = next_event.scheduled_time
        return events_happened

