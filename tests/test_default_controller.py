# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from vl.models.api_response import ApiResponse  # noqa: E501
from vl.models.error import Error  # noqa: E501
from vl.models.user import User  # noqa: E501
from vl.models.user_data_response import UserDataResponse  # noqa: E501
from vl.models.user_id import UserId  # noqa: E501
from vl.models.user_verification_response import UserVerificationResponse  # noqa: E501
from . import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_send_user_data(self):
        """Test case for send_user_data


        """
        body = User()
        response = self.client.open(
            '/v1/user/sendUserData',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_identity(self):
        """Test case for upload_identity


        """
        data = dict(user_id='user_id_example',
                    identity_image='identity_image_example')
        response = self.client.open(
            '/v1/image/uploadIdentity',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_profile(self):
        """Test case for upload_profile


        """
        data = dict(user_id='user_id_example',
                    profile_image='profile_image_example')
        response = self.client.open(
            '/v1/image/uploadProfile',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_verify(self):
        """Test case for verify


        """
        body = UserId()
        response = self.client.open(
            '/v1/user/verify',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
