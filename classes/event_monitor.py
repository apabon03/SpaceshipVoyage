import random
from collections import deque

class DGIMBucket:
    def __init__(self, timestamp, count):
        self.timestamp = timestamp
        self.count = count

class DGIMAlgorithm:
    def __init__(self, N):
        self.N = N
        self.buckets = deque()
        self.next_timestamp = 0

    def update(self, bit):
        if bit == "1":
            new_bucket = DGIMBucket(self.next_timestamp, 1)
            self.buckets.appendleft(new_bucket)

        # Remove old buckets
        while self.buckets and self.buckets[-1].timestamp <= self.next_timestamp - self.N:
            self.buckets.pop()

        # Merge buckets
        i = 0
        while i < len(self.buckets) - 2:
            if self.buckets[i].count == self.buckets[i + 1].count == self.buckets[i + 2].count:
                self.buckets[i + 1].count += self.buckets[i + 2].count
                del self.buckets[i + 2]
            else:
                i += 1

        self.next_timestamp += 1

    def estimate(self):
        estimate = 0
        for bucket in list(self.buckets)[:-1]:
            estimate += bucket.count
        if self.buckets:
            estimate += self.buckets[-1].count // 2
        return estimate

class ControlledBitStreamGenerator:
    def __init__(self, length, percentage_of_ones):
        self.length = length
        self.percentage_of_ones = percentage_of_ones

    def generate(self):
        return "".join(
            "1" if random.random() < self.percentage_of_ones else "0"
            for _ in range(self.length)
        )

class SpaceEventMonitor:
    def __init__(self, window_size):
        self.window_size = window_size
        self.events = {}
        self.bit_generators = {}
        self.alert_thresholds = {}

    def add_event(self, event_name, percentage_of_ones, alert_threshold):
        self.events[event_name] = DGIMAlgorithm(self.window_size)
        self.bit_generators[event_name] = ControlledBitStreamGenerator(length=50, percentage_of_ones=percentage_of_ones)
        self.alert_thresholds[event_name] = alert_threshold

    def load_events_from_json(self, json_data):
        for event_name, data in json_data.items():
            percentage_of_ones = data.get("percentage_of_ones", 0.05)
            alert_threshold = data.get("alert_threshold", 10)
            self.add_event(event_name, percentage_of_ones, alert_threshold)

    def update_event(self, event_name, bit):
        if event_name in self.events:
            self.events[event_name].update(bit)

    def check_alert(self, event_name):
        estimate = self.events[event_name].estimate()
        if estimate >= self.alert_thresholds[event_name]:
            print(f"Alert! {event_name} has reached the critical threshold: {estimate} occurrences.")

    def get_estimates(self):
        estimates = {}
        for event_name, dgim in self.events.items():
            estimate = dgim.estimate()
            estimates[event_name] = estimate
            self.check_alert(event_name)
        return estimates

class EventDataUpdater:
    def __init__(self, monitor):
        self.monitor = monitor

    def distribute_updates(self, total_bits):
        event_names = list(self.monitor.events.keys())
        bits_per_event = total_bits // len(event_names) if event_names else 0
        for event_name in event_names:
            generator = self.monitor.bit_generators[event_name]
            for _ in range(bits_per_event):
                new_bits = generator.generate()
                for bit in new_bits:
                    self.monitor.update_event(event_name, bit)
