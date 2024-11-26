class Person:
    def __init__(self, name, surname, age, gender, family_id, civil_status, children, trips_achieved, salary):
        self.name = name
        self.surname = surname
        self.age = age
        self.gender = gender
        self.family_id = family_id
        self.civil_status = civil_status
        self.children = children
        self.trips_achieved = trips_achieved
        self.salary = salary

    def is_minor(self):
        return self.age < 18

    def __repr__(self):
        return f"{self.name} {self.surname}, Age: {self.age}, FamilyID: {self.family_id}"
