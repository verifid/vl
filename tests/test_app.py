#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tornado.web
import json
import requests

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from vl import (
    InformationHandler,
    UploadImageHandler
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
        return Application([(r'/userData', InformationHandler),
                        (r'/uploadImage', UploadImageHandler)], debug=True, autoreload=False)

    def test_post_informations_success(self):
        post_data = {"name": "Tony",
                     "surname": "Stark",
                     "gender": "M",
                     "date_of_birth": "1980-10-01T00:00:00Z",
                     "place_of_birth": "New York",
                     "country": "USA"}
        body = urlencode(post_data)
        response = self.fetch(r'/userData', method='POST', body=body)
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'{"error": false, "message": "Values received!"}')

    def test_post_informations_fail(self):
        post_data = {"name": "Tony",
                     "surname": "Stark",
                     "gender": "M",
                     "date_of_birth": "1980-10-01T00:00:00Z",
                     "place_of_birth": "New York"}
        body = urlencode(post_data)
        response = self.fetch(r'/userData', method='POST', body=body)
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, b'{"error": true, "message": "Missing values"}')

    def test_post_informations_fail_with_missing_value(self):
        post_data = {"name": "Tony",
                     "surname": None,
                     "gender": "M",
                     "date_of_birth": "1980-10-01T00:00:00Z",
                     "place_of_birth": "New York"}
        body = urlencode(post_data)
        response = self.fetch(r'/userData', method='POST', body=body)
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, b'{"error": true, "message": "Missing values"}')

    def test_post_image(self):
        fpath = os.path.join(os.path.dirname(__file__), 'resources/test.png')
        image_file = open(fpath, 'rb')
        files = {'image': image_file}
        data = {}
        request = requests.Request(url="http://localhost", files=files, data=data)
        prepare = request.prepare()
        content_type = prepare.headers.get('Content-Type')
        body = prepare.body
        url = r'/uploadImage'
        headers = {
            "Content-Type": content_type,
        }
        response = self.fetch(url, method='POST', body=body, headers=headers)
        self.assertEqual(response.code, 200)
