"""Exact cache: only leading/trailing whitespace is removed. Single event loop."""
import hashlib
import time
from collections import OrderedDict

def normalize(message):
    return message.strip()

def cache_key(message):
    return hashlib.sha256(('stub-v1|contract-v1|'+normalize(message)).encode()).hexdigest()

class ExactCache:
    def __init__(self, ttl=600, capacity=1024, clock=time.monotonic):
        if ttl <= 0 or capacity < 1:
            raise ValueError('positive TTL and capacity required')
        self.ttl, self.capacity, self.clock = ttl, capacity, clock
        self.rows = OrderedDict()
        self.hits = self.misses = 0

    def get(self, message):
        key = cache_key(message)
        row = self.rows.get(key)
        if row and row[0] > self.clock():
            self.hits += 1
            self.rows.move_to_end(key)
            return row[1].model_copy(deep=True)
        self.rows.pop(key, None)
        self.misses += 1
        return None

    def put(self, message, response):
        key = cache_key(message)
        self.rows[key] = (self.clock()+self.ttl, response.model_copy(deep=True))
        self.rows.move_to_end(key)
        while len(self.rows) > self.capacity:
            self.rows.popitem(last=False)

    @property
    def hit_rate(self):
        total = self.hits+self.misses
        return self.hits/total if total else 0.0
