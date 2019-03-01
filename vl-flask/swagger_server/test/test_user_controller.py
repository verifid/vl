# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_user_data(self):
        """Test case for user_data

        Creates a user for verification.
        """
        body = User.from_dict({
                    'name': 'Tony',
                    'surname': 'Stark',
                    'gender': 'M',
                    'dateOfBirth': '1980-10-01T00:00:00Z',
                    'placeOfBirth': 'New York',
                    'country': 'USA'
                })
        response = self.client.open(
            '/v1/userData',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
