# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestImageController(BaseTestCase):
    """ImageController integration test stubs"""

    def test_upload_file(self):
        """Test case for upload_file

        Uploads an image
        """
        data = dict(userId='userId_example',
                    file=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/v1/uploadImage',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
