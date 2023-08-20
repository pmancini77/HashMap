def contains_key(self, key: str) -> bool:
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
            return False
        if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
            return True
        else:
            return True


    m = HashMap(10, hash_function_3)
    m.put('a', 1)
    m.put('to', 2)
    m.put('too', 3)
    m.put('cat', 'B')
    m.remove('too')
    m.remove('cat')
    print(m)