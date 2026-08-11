import math
import mmh3
from bitarray import bitarray
from app.database.connection import get_db


class BloomFilter(object):

    def __init__(self, items_count, fp_prob):
        '''
        items_count : int [Size of bit array]
            Number of items expected to be stored in bloom filter
        fp_prob : float
            False Positive probability in decimal
        '''
        self.fp_prob = fp_prob
        items_count = max(1, items_count)
        self.size = self.get_size(items_count, fp_prob)
        self.hash_count = max(1, self.get_hash_count(self.size, items_count))
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

    def add(self, item):
        """Add an item to the filter."""
        item = str(item)
        for seed in range(self.hash_count):
            value = mmh3.hash(item, seed, signed=False) % self.size
            self.bit_array[value] = True

    def check(self, item):
        """Return whether an item may be present in the filter."""
        item = str(item)
        for seed in range(self.hash_count):
            value = mmh3.hash(item, seed, signed=False) % self.size
            if not self.bit_array[value]:
                return False
        return True

    def false_positive_probability(self, inserted_items):
        """Return the expected false-positive probability for the current filter."""
        return (1 - math.exp(
            -self.hash_count * inserted_items / self.size
        )) ** self.hash_count

    @staticmethod
    def get_size(n, p):
        """Return the required bit-array size for n items and probability p."""
        return max(1, int(-(n * math.log(p)) / (math.log(2) ** 2)))

    @staticmethod
    def get_hash_count(m, n):
        """Return the number of hash functions required by the filter."""
        return int((m / n) * math.log(2))


class DatabaseEmailBloomFilter:
    
    def __init__(self, fp_prob=0.05):
        self.fp_prob = fp_prob
        self._filter = None

    def refresh(self):
        with get_db() as (conn, cursor):
            query = "SELECT email FROM Users"
            cursor.execute(query)
            emails = [row["email"] for row in cursor.fetchall()]

        self._filter = BloomFilter(max(1, len(emails)), self.fp_prob)
        for email in emails:
            self._filter.add(email)
        return len(emails)

    def add(self, email):
        """Add a newly-created email without rebuilding the filter."""
        if self._filter is None:
            self.refresh()
        self._filter.add(email)

    def might_contain(self, email):
        """Return False only when the database definitely lacks this email."""
        if self._filter is None:
            self.refresh()
        return self._filter.check(email)
