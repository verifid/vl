# coding: utf-8

from __future__ import absolute_import

import os
import fakeredis
import base64

from flask import json
from six import BytesIO
from shutil import copy2

from vl.store.redis_store import RedisStore
from vl.models.api_response import ApiResponse  # noqa: E501
from vl.models.error import Error  # noqa: E501
from vl.models.user import User  # noqa: E501
from vl.models.user_data_response import UserDataResponse  # noqa: E501
from vl.models.user_id import UserId  # noqa: E501
from vl.models.verify_user import VerifyUser
from vl.models.user_verification_response import UserVerificationResponse  # noqa: E501
from vl.models.image_upload import ImageUpload  # noqa: E501
from . import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""


    def test_send_user_data_success(self):
        """Test case for send_user_data
        """
        body = User(name='Tony',
                    surname='Stark',
                    date_of_birth='1980-10-01T00:00:00Z',
                    country='USA')
        response = self.client.open(
            '/v1/user/sendUserData',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_send_user_data_fail(self):
        """Test case for send_user_data
        """
        response = self.client.open(
            '/v1/user/sendUserData',
            method='POST',
            data=None,
            content_type='application/json')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_send_user_data_fail_with_missing_value(self):
        """Test case for send_user_data
        """
        body = User(name='Tony',
                    surname=None,
                    date_of_birth='1980-10-01T00:00:00Z',
                    country='USA')
        response = self.client.open(
            '/v1/user/sendUserData',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_upload_identity_success(self):
        """Test success case for upload identity.

        Uploads an identity image.
        """
        redis = fakeredis.FakeStrictRedis()
        store = RedisStore(redis)
        user = self.create_user()
        store.keep('userId', json.dumps(user))
        image_path = os.path.dirname(os.path.realpath(__file__)) + '/resources/sample_uk_identity_card.png'
        with open(image_path, 'rb') as imageFile:
            image_data = base64.b64encode(imageFile.read()).decode('utf-8')
        body = ImageUpload()
        body.user_id = "userId"
        body.image = image_data
        response = self.client.open(
            '/v1/image/uploadIdentity',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_upload_identity_fail(self):
        """Test fail case for upload identity.

        Uploads an identity image and fails.
        """
        body = ImageUpload()
        body.user_id = "userId"
        response = self.client.open(
            '/v1/image/uploadIdentity',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_upload_profile_success(self):
        """Test success case for upload profile.

        Uploads a profile image.
        """
        redis = fakeredis.FakeStrictRedis()
        store = RedisStore(redis)
        user = self.create_user()
        store.keep('userId', json.dumps(user))
        image_path = os.path.dirname(os.path.realpath(__file__)) + '/resources/profile.jpg'
        with open(image_path, 'rb') as imageFile:
            image_data = base64.b64encode(imageFile.read()).decode('utf-8')
        body = ImageUpload()
        body.user_id = "userId"
        body.image = image_data
        response = self.client.open(
            '/v1/image/uploadProfile',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_upload_profile_fail(self):
        """Test fail case for upload identity.

        Uploads an profile image and fails.
        """
        body = ImageUpload()
        body.user_id = "userId"
        response = self.client.open(
            '/v1/image/uploadProfile',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_verify_fail_with_invalid_user(self):
        """Test case for verify

        Verifies user.
        """
        body = VerifyUser()
        body.user_id = 'invalid_user_id'
        body.language = 'en_core_web_sm'
        response = self.client.open(
            '/v1/user/verify',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def test_verify_success_with_valid_user(self):
        """Test case for verify

        Verifies user.
        """
        user_id = 'userId'
        directory = os.getcwd() + '/testsets/' + 'identity' + '/' + user_id + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        src_image_path = os.path.dirname(os.path.realpath(__file__)) + '/resources/sample_uk_identity_card.png'
        copy2(src_image_path, directory)
        os.rename(directory + '/sample_uk_identity_card.png', directory + 'image.png')

        body = VerifyUser()
        body.user_id = user_id
        body.language = 'en_core_web_sm'
        redis = fakeredis.FakeStrictRedis()
        store = RedisStore(redis)
        user = self.create_user()
        store.keep(user_id, json.dumps(user))
        response = self.client.open(
            '/v1/user/verify',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


    def create_user(self):
        user = User()
        user.name = 'Elizabeth'
        user.surname = 'Green'
        user.country = 'United Kingdom'
        user.date_of_birth = '14.04.1977'
        return user

if __name__ == '__main__':
    import unittest
    unittest.main()
