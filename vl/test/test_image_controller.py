# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from vl.models.api_response import ApiResponse  # noqa: E501
from test import BaseTestCase


class TestImageController(BaseTestCase):
    """ImageController integration test stubs"""

    def test_upload_image_success(self):
        """Test success case for upload_file.

        Uploads an image
        """

        data = dict(userId='userId_example',
                    file=(BytesIO(b'some file data'), 'test.png'))
        response = self.client.open(
            '/v1/image/upload',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_image_fail(self):
        """Test fail case for upload_file.

        Uploads an image
        """

        data = dict(userId='userId_example',
                    file=None)
        response = self.client.open(
            '/v1/image/upload',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
