class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size

    def _hashes(self, item):
        hash_results = []
        item_str = str(item).encode('utf-8')
        for i in range(self.hash_count):
            hash_result = (hash(item_str) + i) % self.size
            hash_results.append(hash_result)
        return hash_results

    def add(self, item):
        for hash_val in self._hashes(item):
            self.bit_array[hash_val] = 1

    def check(self, item):
        for hash_val in self._hashes(item):
            if self.bit_array[hash_val] == 0:
                return False
        return True
