import hashlib
import inspect
import pickle
import time
from functools import wraps


class Cache(object):
    def __init__(self, maxsize=255, ttl=10):
        self.__maxsize = maxsize
        self.__ttl = ttl

        self.__cache = {}

    def hash(self, func):
        hashkey = pickle.dumps((func.__name__))
        return hashlib.sha1(hashkey).hexdigest()

    def isobsolete(self, key):
        return time.time()-self.__cache[key]['time'] > self.__cache[key]['ttl']

    @property
    def isfull(self):
        return len(self.__cache) >= self.__maxsize

    def set(self, hashkey, value, ttl=None):
        if not self.isfull:
            if ttl is None:
                ttl = self.__ttl
            if hashkey in self.__cache.keys():
                if value is not self.__cache[hashkey]:
                    self.__cache[hashkey] = {
                        'value': value, 'ttl': ttl, 'time': time.time()}
            else:
                self.__cache[hashkey] = {'value': value,
                                         'ttl': ttl, 'time': time.time()}
        else:
            print('Cache is Full.')
            return

    def get(self, key):
        hashkey = self.hash(key)
        if hashkey in self.__cache.keys():
            return self.__cache[hashkey]['value']
        else:
            return None

    def cache(self, ttl=None):
        if ttl is None:
            ttl = self.__ttl

        def wrap(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                hashkey = self.hash(func)
                val = func(*args, **kwargs)
                self.set(hashkey, val, ttl=ttl)
            return wrapper
        return wrap

    def viewcache(self):
        print(self.__cache)
