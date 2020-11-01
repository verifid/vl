#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import fakeredis

from vl.store.redis_store import RedisStore


class RedisStoreTest(unittest.TestCase):
    def setUp(self):
        self.redis = fakeredis.FakeStrictRedis()
        self.store = RedisStore(self.redis)

    def test_initiation(self):
        self.assertIsNotNone(self.store)

    def test_keep(self):
        self.store.keep("key", "value")
        value = self.store.value_of("key")
        self.assertEqual(value, "value")
