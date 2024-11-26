import random
from classes.cabin import Cabin

def group_people_by_family(people):
    families = {}
    for person in people:
        family_id = person.family_id
        if family_id not in families:
            families[family_id] = []
        families[family_id].append(person)
    return families

def create_cabins(total_cabins, max_capacity):
    return [Cabin(cabin_id=i+1, max_capacity=max_capacity) for i in range(total_cabins)]

def allocate_families_to_cabins(families, cabins, bloom_filter):
    cabin_index = 0
    total_cabins = len(cabins)

    # Convert families dict to a list and shuffle to randomize allocation
    family_list = list(families.values())
    random.shuffle(family_list)

    for family_members in family_list:
        family_id = family_members[0].family_id

        # Check if family has already been allocated
        if bloom_filter.check(str(family_id)):
            continue  # Family already allocated

        # Separate minors and adults
        minors = [p for p in family_members if p.is_minor()]
        adults = [p for p in family_members if not p.is_minor()]

        if adults:
            # Allocate adults
            for adult in adults:
                allocated = False
                while not allocated and cabin_index < total_cabins:
                    cabin = cabins[cabin_index]
                    if cabin.has_space():
                        cabin.add_person(adult)
                        allocated = True
                    else:
                        cabin_index += 1
                if not allocated:
                    print("No more space to allocate adults.")
                    return

            # Allocate minors with their family's adults
            for minor in minors:
                allocated = False
                for cabin in cabins:
                    if cabin.has_space() and cabin.contains_family(family_id):
                        cabin.add_person(minor)
                        allocated = True
                        break
                if not allocated:
                    print(f"No space to allocate minor {minor.name} from family {family_id}.")
        else:
            # Cannot allocate minors without an adult from their family
            print(f"Cannot allocate minors of family {family_id} without an adult from their family.")
            continue

        # Add the family to the Bloom filter
        bloom_filter.add(str(family_id))

def allocate_resources_to_cabins(resources, cabins):
    random.shuffle(resources)
    cabin_index = 0
    num_cabins = len(cabins)
    for resource in resources:
        cabins[cabin_index].resources.append(resource)
        cabin_index = (cabin_index + 1) % num_cabins
