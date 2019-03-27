# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from vl.models.user import User
from vl.models.user_id import UserId
from . import BaseTestCase

class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_send_data_success(self):
        """Test success case for send_data

        Creates a user for verification.
        """

        body = {'name': 'Tony',
                'surname': 'Stark',
                'gender': 'M',
                'dateOfBirth': '1980-10-01T00:00:00Z',
                'placeOfBirth': 'New York',
                'country': 'USA'}
        response = self.client.open(
            '/v1/user/sendData',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_send_data_fail(self):
        """Test error case for send_data

        Creates a user for verification.
        """

        response = self.client.open(
            '/v1/user/sendData',
            method='POST',
            data=None,
            content_type='application/json')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_send_data_fail_with_missing_value(self):
        """Test error case for send_data

        Creates a user for verification.
        """

        body = {"name": "Tony",
                "surname": None,
                "gender": "M",
                "date_of_birth": "1980-10-01T00:00:00Z",
                "place_of_birth": "New York"}
        response = self.client.open(
            '/v1/user/sendData',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_verify_fail_with_invalid_user(self):
        """Test case for verify

        Verifies user.
        """

        body = UserId()
        body.user_id = 'userId'
        response = self.client.open(
            '/v1/user/verify',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

if __name__ == '__main__':
    import unittest
    unittest.main()
