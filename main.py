from utils.data_loading import load_people_from_json, generate_resources
from utils.allocation import (
    group_people_by_family,
    create_cabins,
    allocate_families_to_cabins,
    allocate_resources_to_cabins,
)
from classes.bloom_filter import BloomFilter

def main():
    # Load people from JSON
    people = load_people_from_json('people.json')

    # Group people into families
    families = group_people_by_family(people)

    # Create cabins
    total_cabins = 100  
    cabin_capacity = 6
    cabins = create_cabins(total_cabins, cabin_capacity)

    # Initialize Bloom filter
    bloom_filter = BloomFilter(size=1000, hash_count=5)

    # Allocate families to cabins
    allocate_families_to_cabins(families, cabins, bloom_filter)

    # Generate resources
    resource_quantities = {
        "Food Supplies": 10,
        "Water": 15,
        "Medical Kits": 5,
        "Oxygen Tanks": 8,
        "Tool Kits": 7,
    }
    resources = generate_resources(resource_quantities)

    # Allocate resources to cabins
    allocate_resources_to_cabins(resources, cabins)

    # Print cabin allocations
    for cabin in cabins:
        print(cabin)
        print("Occupants:")
        for occupant in cabin.occupants:
            print(f"  - {occupant}")
        print("Resources:")
        for resource in cabin.resources:
            print(f"  - {resource}")
        print()

if __name__ == "__main__":
    main()
