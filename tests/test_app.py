#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tornado.web

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

    def test_post_informations(self):
        post_data = {'name': 'Tony',
                     'surname': 'Stark',
                     'sex': 'M',
                     'date_of_birth': '10.01.1980',
                     'place_of_birth': 'London',
                     'country': 'USA'}
        body = urlencode(post_data)
        response = self.fetch(r'/informations', method='POST', body=body)
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'{"country": "USA", "date_of_birth": "10.01.1980", "name": "Tony", "place_of_birth": "London", "sex": "M", "surname": "Stark"}')
