# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from vl.models.base_model_ import Model
from vl import util


class Body(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, user_id: str=None, profile_image: str=None):  # noqa: E501
        """Body - a model defined in Swagger

        :param user_id: The user_id of this Body.  # noqa: E501
        :type user_id: str
        :param profile_image: The profile_image of this Body.  # noqa: E501
        :type profile_image: str
        """
        self.swagger_types = {
            'user_id': str,
            'profile_image': str
        }

        self.attribute_map = {
            'user_id': 'userId',
            'profile_image': 'profileImage'
        }
        self._user_id = user_id
        self._profile_image = profile_image

    @classmethod
    def from_dict(cls, dikt) -> 'Body':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The body of this Body.  # noqa: E501
        :rtype: Body
        """
        return util.deserialize_model(dikt, cls)

    @property
    def user_id(self) -> str:
        """Gets the user_id of this Body.


        :return: The user_id of this Body.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: str):
        """Sets the user_id of this Body.


        :param user_id: The user_id of this Body.
        :type user_id: str
        """

        self._user_id = user_id

    @property
    def profile_image(self) -> str:
        """Gets the profile_image of this Body.


        :return: The profile_image of this Body.
        :rtype: str
        """
        return self._profile_image

    @profile_image.setter
    def profile_image(self, profile_image: str):
        """Sets the profile_image of this Body.


        :param profile_image: The profile_image of this Body.
        :type profile_image: str
        """

        self._profile_image = profile_image