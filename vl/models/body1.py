# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from vl.models.base_model_ import Model
from vl import util


class Body1(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, user_id: str=None, identity_image: str=None):  # noqa: E501
        """Body1 - a model defined in Swagger

        :param user_id: The user_id of this Body1.  # noqa: E501
        :type user_id: str
        :param identity_image: The identity_image of this Body1.  # noqa: E501
        :type identity_image: str
        """
        self.swagger_types = {
            'user_id': str,
            'identity_image': str
        }

        self.attribute_map = {
            'user_id': 'userId',
            'identity_image': 'identityImage'
        }
        self._user_id = user_id
        self._identity_image = identity_image

    @classmethod
    def from_dict(cls, dikt) -> 'Body1':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The body_1 of this Body1.  # noqa: E501
        :rtype: Body1
        """
        return util.deserialize_model(dikt, cls)

    @property
    def user_id(self) -> str:
        """Gets the user_id of this Body1.


        :return: The user_id of this Body1.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: str):
        """Sets the user_id of this Body1.


        :param user_id: The user_id of this Body1.
        :type user_id: str
        """

        self._user_id = user_id

    @property
    def identity_image(self) -> str:
        """Gets the identity_image of this Body1.


        :return: The identity_image of this Body1.
        :rtype: str
        """
        return self._identity_image

    @identity_image.setter
    def identity_image(self, identity_image: str):
        """Sets the identity_image of this Body1.


        :param identity_image: The identity_image of this Body1.
        :type identity_image: str
        """

        self._identity_image = identity_image
