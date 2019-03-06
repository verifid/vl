# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from vl.models.api_response import ApiResponse  # noqa: E501
from . import BaseTestCase

class TestImageController(BaseTestCase):
    """ImageController integration test stubs"""

    def test_upload_identity_success(self):
        """Test success case for upload identity.

        Uploads an identity image.
        """

        data = dict(userId='userId_example',
                    file=(BytesIO(b'some file data'), 'test.png'))
        response = self.client.open(
            '/v1/image/uploadIdentity',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_identity_fail(self):
        """Test fail case for upload identity.

        Uploads an identity image and fails.
        """

        data = dict(userId='userId_example',
                    file=None)
        response = self.client.open(
            '/v1/image/uploadIdentity',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_profile_success(self):
        """Test success case for upload profile.

        Uploads a profile image.
        """

        data = dict(userId='userId_example',
                    file=(BytesIO(b'some file data'), 'test.png'))
        response = self.client.open(
            '/v1/image/uploadProfile',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_profile_fail(self):
        """Test fail case for upload identity.

        Uploads an profile image and fails.
        """

        data = dict(userId='userId_example',
                    file=None)
        response = self.client.open(
            '/v1/image/uploadProfile',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
