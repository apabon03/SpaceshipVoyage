import random

class Resource:
    def __init__(self, resource_id, name):
        self.resource_id = resource_id
        self.name = name
        self.random_key = random.random()

    def __lt__(self, other):
        return self.random_key < other.random_key

    def __repr__(self):
        return f"Resource(ID: {self.resource_id}, Name: {self.name})"
