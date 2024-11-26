import unittest
from classes.person import Person
from classes.cabin import Cabin
from classes.bloom_filter import BloomFilter
from utils.allocation import group_people_by_family, create_cabins, allocate_families_to_cabins

class TestSpaceshipAllocation(unittest.TestCase):
    def test_person_is_minor(self):
        minor = Person("John", "Doe", 17, "Male", 1, "Single", 0, 0, 5000)
        adult = Person("Jane", "Doe", 30, "Female", 1, "Married", 2, 5, 8000)
        self.assertTrue(minor.is_minor())
        self.assertFalse(adult.is_minor())

    def test_cabin_add_person(self):
        cabin = Cabin(1, 2)
        person1 = Person("Alice", "Smith", 25, "Female", 2, "Single", 0, 3, 6000)
        person2 = Person("Bob", "Smith", 28, "Male", 2, "Married", 1, 4, 7000)
        self.assertTrue(cabin.add_person(person1))
        self.assertTrue(cabin.add_person(person2))
        self.assertFalse(cabin.add_person(person1))  # Cabin is full

    def test_bloom_filter(self):
        bloom_filter = BloomFilter(size=10, hash_count=2)
        bloom_filter.add("family_1")
        self.assertTrue(bloom_filter.check("family_1"))
        self.assertFalse(bloom_filter.check("family_2"))

    def test_allocate_families_to_cabins(self):
        people = [
            Person("Adult1", "Family1", 30, "Male", 1, "Single", 0, 5, 8000),
            Person("Minor1", "Family1", 15, "Female", 1, "Single", 0, 0, 0),
            Person("Adult2", "Family2", 40, "Female", 2, "Married", 1, 10, 9000),
            Person("Minor2", "Family2", 10, "Male", 2, "Single", 0, 0, 0),
            Person("Minor3", "Family3", 12, "Male", 3, "Single", 0, 0, 0),  # No adult in family 3
        ]
        families = group_people_by_family(people)
        cabins = create_cabins(2, 3)
        bloom_filter = BloomFilter(size=100, hash_count=3)
        allocate_families_to_cabins(families, cabins, bloom_filter)
        # Check that minors from family 3 were not allocated
        allocated_family_ids = set()
        for cabin in cabins:
            for occupant in cabin.occupants:
                allocated_family_ids.add(occupant.family_id)
        self.assertNotIn(3, allocated_family_ids)

if __name__ == '__main__':
    unittest.main()
