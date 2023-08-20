# Name: paul mancini
# OSU Email: mancinip@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Portfolio assignment Hash Maps
# Due Date: 8/15
# Description: Implementing a hash map using open addressing

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """takes in a key and a value and assigns them to an appropriate index"""
        hash = self._hash_function(key)
        index = hash % self._capacity
        lf = self.table_load()
        if lf >= 0.5:
            self.resize_table(self._capacity * 2)
            index = hash % self._capacity
        con_key = self.contains_key(key)
        con_tomb = self.contains_tombstone(key)
        if con_key:
            if self._buckets[index].key == key:
                self._buckets[index].value = value
            else:
                index = self.quad_probe_val(index, key)
                self._buckets[index].value = value
        elif con_tomb:
            con_tomb.value = value
            con_tomb.is_tombstone = False
            self._size += 1
        else:
            if self._buckets[index] is None or self._buckets[index].is_tombstone is True:
                self._buckets[index] = HashEntry(key, value)
                self._size += 1
            else:
                index = self.quad_probe_empty(index)
                self._buckets[index] = HashEntry(key, value)
                self._size += 1

    def quad_probe_empty(self, initial):
        """probes the hashmap for an empty spot"""
        j = 1
        index = (initial + j ** 2) % self._capacity
        while self._buckets[index]:
                j += 1
                index = (initial + j ** 2) % self._capacity
        return index

    def table_load(self) -> float:
        """returns the load factor"""
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """returns the empty buckets amount"""
        mt_bucks = self._capacity - self._size
        return mt_bucks

    def resize_table(self, new_capacity: int) -> None:
        """doubles (rounded to nearest prime) capacity of hashmap"""
        if new_capacity < self._size:
            return
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
        old_bucket = self._buckets
        self._capacity = new_capacity
        self.clear()
        self._size = 0
        for index in range(old_bucket.length()):
            if old_bucket[index] is not None and old_bucket[index].is_tombstone is False:
                self.put(old_bucket[index].key, old_bucket[index].value)

    def get(self, key: str) -> object:
        """returns a value of associated key"""
        hash = self._hash_function(key)
        index = hash % self._capacity
        if self._buckets[index] is None or self._buckets[index].is_tombstone is True:
            return None
        if self._buckets[index].key == key:
            return self._buckets[index].value
        else:
            index = self.quad_probe_val(index, key)
            if self._buckets[index] is None or self._buckets[index].is_tombstone is True:
                return None
            else:
                return self._buckets[index].value

    def quad_probe_val(self, initial, key):
        """searches the hashmap for appropriate key"""
        j = 1
        index = (initial + j ** 2) % self._capacity
        while self._buckets[index]:
            if self._buckets[index].key == key:
                return index
            else:
                j += 1
                index = (initial + j ** 2) % self._capacity
        return index

    def contains_key(self, key: str) -> bool:
        """returns true or false if key is present"""
        hash = self._hash_function(key)
        index = hash % self._capacity
        if self._buckets[index] is None:
            return False
        if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
            return True
        else:
            index = self.quad_probe_val(index, key)
            if self._buckets[index] is None:
                return False
            if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                return True
            if self._buckets[index].key == key and self._buckets[index].is_tombstone is True:
                return False
            else:
                return True

    def contains_tombstone(self, key:str):
        """searches for a tombstone value"""
        hash = self._hash_function(key)
        index = hash % self._capacity
        if self._buckets[index] is None:
            return False
        if self._buckets[index].key == key and self._buckets[index].is_tombstone is True:
            return self._buckets[index]
        else:
            index = self.quad_probe_val(index, key)
            if self._buckets[index] is None:
                return False
            if self._buckets[index] and self._buckets[index].is_tombstone is True:
                return self._buckets[index]

    def remove(self, key: str) -> None:
        """creates tombstones"""
        hash = self._hash_function(key)
        index = hash % self._capacity
        con_key = self.contains_key(key)
        if not con_key:
            return
        if self._buckets[index].key == key:
            self._buckets[index].is_tombstone = True
            self._size -= 1
        else:
            index = self.quad_probe_val(index, key)
            tomb = self._buckets[index]
            tomb.is_tombstone = True
            self._size -= 1
                #self._buckets[index].is_tombstone = True
                #self._size -= 1

    def clear(self) -> None:
        """clears dynamic array"""
        self._buckets = DynamicArray()
        self._size = 0
        for _ in range(self._capacity):
            self._buckets.append(None)

    def get_keys_and_values(self) -> DynamicArray:
        """returns all keys and values"""
        key_val = DynamicArray()
        for val in self:
            if val.is_tombstone is False:
                key_val.append((val.key, val.value))
        return key_val

    def __iter__(self):
        """init iterator"""
        self._index = 0

        return self

    def __next__(self):
        """next value in iterator"""
        try:
                value = self._buckets[self._index]
                while value is None or value.is_tombstone is True:
                    self._index += 1
                    value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration


        self._index = self._index + 1
        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
