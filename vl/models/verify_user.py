# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from vl.models.base_model_ import Model
from vl import util


class VerifyUser(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, user_id: str = None, language: str = None):  # noqa: E501
        """VerifyUser - a model defined in Swagger

        :param user_id: The user_id of this VerifyUser.  # noqa: E501
        :type user_id: str
        :param language: The language of this VerifyUser.  # noqa: E501
        :type language: str
        """
        self.swagger_types = {"user_id": str, "language": str}

        self.attribute_map = {"user_id": "userId", "language": "language"}
        self._user_id = user_id
        self._language = language

    @classmethod
    def from_dict(cls, dikt) -> "VerifyUser":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The VerifyUser of this VerifyUser.  # noqa: E501
        :rtype: VerifyUser
        """
        return util.deserialize_model(dikt, cls)

    @property
    def user_id(self) -> str:
        """Gets the user_id of this VerifyUser.


        :return: The user_id of this VerifyUser.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: str):
        """Sets the user_id of this VerifyUser.


        :param user_id: The user_id of this VerifyUser.
        :type user_id: str
        """
        if user_id is None:
            raise ValueError(
                "Invalid value for `user_id`, must not be `None`"
            )  # noqa: E501

        self._user_id = user_id

    @property
    def language(self) -> str:
        """Gets the language of this VerifyUser.


        :return: The language of this VerifyUser.
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language: str):
        """Sets the language of this VerifyUser.


        :param language: The language of this VerifyUser.
        :type language: str
        """
        if language is None:
            raise ValueError(
                "Invalid value for `language`, must not be `None`"
            )  # noqa: E501

        self._language = language
