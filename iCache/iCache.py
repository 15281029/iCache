import hashlib
import json
import pickle
import time
from functools import wraps


class Cache(object):
    def __init__(self, maxsize=255, ttl=10):
        self.__maxsize = maxsize
        self.__ttl = ttl

        self.__cache = {}

    def __getitem__(self, key):
        return self.get_value(key)

    def __len__(self):
        return len(self.__cache)

    def hash(self, func):
        if not hasattr(func, '__name__'):
            hashkey = pickle.dumps((func))
        else:
            hashkey = pickle.dumps((func.__name__))
        return hashlib.sha1(hashkey).hexdigest()

    def is_effective(self, key):
        if not hasattr(key, '__name__'):
            hashkey = key
        else:
            hashkey = self.hash(key)
        if hashkey in self.__cache:
            return time.time()-self.__cache[hashkey]['time'] < self.__cache[hashkey]['ttl']
        else:
            return None

    @property
    def is_full(self):
        return len(self.__cache) >= self.__maxsize

    def set(self, hashkey, value, ttl=None):
        if not self.is_full:
            if ttl is None:
                ttl = self.__ttl
            if hashkey in self.__cache.keys():
                if value is not self.__cache[hashkey]:
                    self.__cache[hashkey] = {
                        'value': value, 'ttl': ttl, 'time': time.time()}
            else:
                self.__cache[hashkey] = {
                    'value': value, 'ttl': ttl, 'time': time.time()}
        else:
            print('Cache is Full.')
            return

    def get_all(self, key):
        if not hasattr(key, '__name__'):
            hashkey = key
        else:
            hashkey = self.hash(key)
        if hashkey in self.__cache.keys():
            return self.__cache[hashkey]
        else:
            return None

    def get_value(self, key):
        if not hasattr(key, '__name__'):
            hashkey = key
        else:
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

    def view_cache(self):
        print(self.__cache)

    def delete(self, key=None, para=None):
        l = []
        if para in ['all', 'invalid', None]:
            if para is None:
                if not hasattr(key, '__name__'):
                    hashkey = key
                else:
                    hashkey = self.hash(key)
                if hashkey in self.__cache:
                    del self.__cache[hashkey]
                else:
                    print('No Cache')
            elif para is 'all':
                self.__cache.clear()
            elif para is 'invalid':
                for i in self.__cache:
                    if not self.is_effective(i):
                        l.append(i)
                for j in l:
                    self.delete(j)
        else:
            print('Parameter Error.')
            return

    def dump(self):
        return json.dumps(self.__cache, ensure_ascii=False)
