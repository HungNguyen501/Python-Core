from torch import long
from typing import NamedTuple, Any

BLANK = Any

class Pair(NamedTuple):
    key: Any
    value: Any

class HashTable:
    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("Capacity must be a positive number")
        self._pairs = capacity*[None]

    def __len__(self):
        return len(self._pairs)

    def _index(self, key):
        return hash(key)%len(self)

    def __setitem__(self, key, value):
        self._pairs[self._index(key)] = Pair(key, value)
    
    def __getitem__(self, key):
        pair = self._pairs[self._index(key)]
        
        if pair is None:
            raise KeyError(key)
        
        return pair.value

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
    
    def __delitem__(self, key):
        if key in self:
            self._pairs[self._index(key)] = None
        else:
            raise KeyError(key)

    def __iter__(self):
        yield from self.keys
    
    @property
    def pairs(self):
        return self._pairs.copy()

    @property
    def keys(self):
        return {pair.key for pair in self.pairs if pair}

    @property
    def values(self):
        return [pair.value for pair in self.pairs if pair]



if __name__=='__main__':
    print(Any)
