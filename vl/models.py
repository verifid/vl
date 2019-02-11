#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jsonobject import *

class UserInformations(JsonObject):
    """Class where we hold user informations temporarly."""

    name = StringProperty(required=True)
    surname = StringProperty(required=True)
    sex = StringProperty(required=True)
    date_of_birth = DateTimeProperty(required=True)
    place_of_birth = StringProperty(required=True)
    country = StringProperty(required=True)
