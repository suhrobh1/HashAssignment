# Name: Suhrob Hasanov
# OSU Email: hasanovs@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/13/23
# Description: AO HashMap implementation  

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
        """
        Adds key/value pair to the hash map.
        """
        load_factor = self._size / self.get_capacity()

        # print(load_factor)
        if load_factor >= 0.5:
            self.resize_table(self.get_capacity() * 2)

        # Hash process to get index
        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        original_index = index

        j = 1
        location = self._buckets[index]

        # While the location is currently busy, continue looking
        while location is not None:
            # If keys match, replace value
            if self._buckets[index].key == key:
                self._buckets[index].value = value
                if self._buckets[index].is_tombstone is True:
                    self._buckets[index].is_tombstone = False
                    self._size += 1
                return
            # Increment index
            index = (original_index + j * j) % self._capacity
            j += 1
            # If index gets higher than capacity (Maybe dont need this check?)
            if index >= self._capacity:
                return
            else:
                location = self._buckets[index]

        # Add the hash entry at given index and increment size
        self._buckets[index] = HashEntry(key, value)
        self._size += 1
        
        

    def table_load(self) -> float:
        """
        Returns load factor of the hash map. 
        """
        load_factor = self._size / self.get_capacity()
        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets of the map.
        """
        return self._capacity - self._size


    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the table with given new capacity.
        """
        # If new capacity is less than size, do nothing
        if new_capacity < self._size:
            return
        
        # If new capacity is not prime, getting prime one
        if self._is_prime(new_capacity) is False:
                new_capacity = self._next_prime(new_capacity)

        # Copying existing array and its capacity
        copy_bucket = self._buckets
        copy_capacity = self._capacity 
        
        # resetting the exisitng array and size
        self._buckets = DynamicArray()
        self._size = 0
        
        # Adding basically placeholders to the reset array
        for _ in range(new_capacity):
            self._buckets.append(None)
        

        # Updating the capacity
        self._capacity = new_capacity

        # Adding the elements from copy of array to the reset array via put function
        for i in range(copy_capacity):
            item = copy_bucket[i]
            if item:
                if item.is_tombstone is False:
                    self.put(item.key, item.value)

        return

    def get(self, key: str) -> object:
        """
        Returns the value associated with passed key.
        """
        # Hash process to get index
        hash = self._hash_function(key)
        size = self.get_capacity()
        index = hash % size

        original_index = index

        j = 1
        location = self._buckets[index]
        # Iterating and probing for open location
        while location is not None:
            if self._buckets[index].key == key:
                # Making sure that item was not previously removed
                if self._buckets[index].is_tombstone is False:
                    return self._buckets[index].value
            index = (original_index + j * j) % self._capacity
            j += 1
            if index >= self._capacity:
                break
            else:
                # Incrementing the location
                location = self._buckets[index]
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns boolean depending whether key is in map.
        """
        # Hash and indexing process
        hash = self._hash_function(key)
        size = self.get_capacity()
        index = hash % size

        original_index = index

        j = 1
        location = self._buckets[index]
        # Iterating and probing correct key
        while location is not None:
            if self._buckets[index].key == key:
                return True
            index = (original_index + j * j) % self._capacity
            j += 1
            if index >= self._capacity:
                break
            else:
                location = self._buckets[index]
        return False


    def remove(self, key: str) -> None:
        """
        Removes key/value pair from the map.
        """
        
        hash = self._hash_function(key)
        size = self.get_capacity()
        index = hash % size

        original_index = index

        j = 1
        location = self._buckets[index]
        while location is not None:
            if self._buckets[index].key == key:
                # If TS is false, need to set to True and decrement size
                if self._buckets[index].is_tombstone is False:
                    self._buckets[index].is_tombstone = True
                    self._size -= 1
                    break
            index = (original_index + j * j) % self._capacity
            j += 1
            if index >= self._capacity:
                break
            else:
                location = self._buckets[index]
        


    def clear(self) -> None:
        """
        Clears the hashmap.
        """
        new_bucket = DynamicArray()
        for i in range(self._capacity):
            new_bucket.append(None)
        self._buckets = new_bucket
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns DynamicArray of key/value pairs in map.
        """
        return_array = DynamicArray()

        for i in range(self._capacity):
            if self._buckets[i]:
                if self._buckets[i].is_tombstone is False:
                    key_pair = (self._buckets[i].key, self._buckets[i].value)
                    return_array.append(key_pair)
        
        return return_array
    

    def __iter__(self):
        """
        Create iterator for loop
        """
        self._index = 0

        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        """
        # print("self._index", self._index, self._capacity)
        if self._index >= self._capacity:
            raise StopIteration

        # Iterating and skipping the empty buckets
        while self._index < self._capacity:
            if self._buckets[self._index] is not None:
                if self._buckets[self._index].is_tombstone == False:
                    value = self._buckets[self._index]
                    self._index = self._index + 1
                    return value
                else:
                    self._index = self._index + 1
            else:
                self._index = self._index + 1
        raise StopIteration 
        
       




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

    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))

    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
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

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))

    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(11, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))

    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)

    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')

    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())

    # m.resize_table(2)
    # print(m.get_keys_and_values())

    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(12)
    # print(m.get_keys_and_values())

    # print("\nPDF - __iter__(), __next__() example 1")
    # print("---------------------")
    # m = HashMap(10, hash_function_1)
    # for i in range(5):
    #     m.put(str(i), str(i * 10))
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)

    # print("\nPDF - __iter__(), __next__() example 2")
    # print("---------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(5):
    #     m.put(str(i), str(i * 24))
    # m.remove('0')
    # m.remove('4')
    # print(m)
    # for item in m:
    #     # print("Here here", item)
    #     print('K:', item.key, 'V:', item.value)
