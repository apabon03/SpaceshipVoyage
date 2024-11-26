class Cabin:
    def __init__(self, cabin_id, max_capacity):
        self.cabin_id = cabin_id
        self.max_capacity = max_capacity
        self.occupants = []
        self.resources = []  # Add this line to include resources

    def has_space(self):
        return len(self.occupants) < self.max_capacity

    def add_person(self, person):
        if self.has_space():
            self.occupants.append(person)
            return True
        return False

    def contains_family(self, family_id):
        return any(person.family_id == family_id for person in self.occupants)

    def __repr__(self):
        return f"Cabin {self.cabin_id}: {len(self.occupants)}/{self.max_capacity} occupants"
