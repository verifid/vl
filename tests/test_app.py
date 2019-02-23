#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tornado.web
import json
import requests

from tornado.testing import (
    AsyncHTTPTestCase,
    gen_test
)
from tornado.web import Application
from urllib.parse import urlunparse

from vl import (
    UserDataHandler,
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
        return Application([(r'/userData', UserDataHandler),
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

    @gen_test(timeout=100)
    def test_post_image(self):
        fpath = os.path.join(os.path.dirname(__file__), 'resources/test.png')
        image_file = open(fpath, 'rb')
        files = {'image': image_file}
        data = {}
        url = urlunparse(('http', 'localhost', '/uploadImage', None, None, None))
        request = requests.Request(url=url, files=files, data=data)
        prepare = request.prepare()
        content_type = prepare.headers.get('Content-Type')
        body = prepare.body
        headers = {
            "Content-Type": content_type,
        }
        response = yield self.http_client.fetch(self.get_url("/uploadImage"), method='POST',
                                        body=body, headers=headers)
        self.assertEqual(response.code, 202)
        self.assertEqual(response.body, b'{"error": false, "message": "Image file received!"}')
