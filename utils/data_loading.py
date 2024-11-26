import json
from classes.person import Person
from classes.resource import Resource

def load_people_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    people = []
    for person_data in data:
        person = Person(
            name=person_data['Name'],
            surname=person_data['Surname'],
            age=person_data['Age'],
            gender=person_data['Gender'],
            family_id=person_data['FamilyID'],
            civil_status=person_data['CivilStatus'],      
            children=person_data['Children'],
            trips_achieved=person_data['TripsAchieved'],  
            salary=person_data['Salary']
        )
        people.append(person)
    return people

def generate_resources(resource_quantities):
    resources = []
    resource_id = 1
    for name, quantity in resource_quantities.items():
        for _ in range(quantity):
            resource = Resource(resource_id=resource_id, name=name)
            resources.append(resource)
            resource_id += 1
    return resources
