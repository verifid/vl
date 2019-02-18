#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tornado.web
import json

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from vl import (
    InformationHandler
)

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

class AppTest(AsyncHTTPTestCase):

    def setUp(self):
        super(AppTest, self).setUp()
        # allow more time before timeout since we are doing remote access..
        os.environ["ASYNC_TEST_TIMEOUT"] = str(20)

    def get_app(self):
        return Application([(r'/informations', InformationHandler)], debug=True, autoreload=False)

    def test_post_informations_success(self):
        post_data = {"name": "Tony",
                     "surname": "Stark",
                     "gender": "M",
                     "date_of_birth": "1980-10-01T00:00:00Z",
                     "place_of_birth": "New York",
                     "country": "USA"}
        body = urlencode(post_data)
        response = self.fetch(r'/informations', method='POST', body=body)
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'{"error": false, "message": "Values received!"}')

    def test_post_informations_fail(self):
        post_data = {"name": "Tony",
                     "surname": "Stark",
                     "gender": "M",
                     "date_of_birth": "1980-10-01T00:00:00Z",
                     "place_of_birth": "New York"}
        body = urlencode(post_data)
        response = self.fetch(r'/informations', method='POST', body=body)
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, b'{"error": true, "message": "Missing values"}')

    def test_post_informations_fail_with_missing_value(self):
        post_data = {"name": "Tony",
                     "surname": None,
                     "gender": "M",
                     "date_of_birth": "1980-10-01T00:00:00Z",
                     "place_of_birth": "New York"}
        body = urlencode(post_data)
        response = self.fetch(r'/informations', method='POST', body=body)
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, b'{"error": true, "message": "Missing values"}')
