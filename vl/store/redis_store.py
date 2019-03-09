#!/usr/bin/env python
# -*- coding: utf-8 -*-

from redis import (
    Redis,
    exceptions
)

class RedisStore(object):
    """Class used to store user datas with unique ids."""

    class __RedisStore:
        def __init__(self, redis):
            self._redis = redis
        def __str__(self):
            return repr(self) + self._redis

    instance = None
 
    def __init__(self, redis):
        if not RedisStore.instance:
            RedisStore.instance = RedisStore.__RedisStore(redis)
        else:
            RedisStore.instance._redis = redis

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def keep(self, key, value):
        try:
            self._redis.set(key, value)
        except exceptions.ConnectionError:
            print('Redis connection error when trying to keep long url')

    def value_of(self, key):
        try:
            url = self._redis.get(key)
            if url:
                return url.decode('utf-8')
            return None
        except exceptions.ConnectionError:
            print('Redis connection error when trying to get long url')
            return None
