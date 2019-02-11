#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import pytest
import datetime

from vl.models import UserInformations

class ModelsTest(unittest.TestCase):

    def test_init_userinformations(self):
        user_informations = UserInformations.wrap({"name": "Tony",
                                                   "surname": "Stark",
                                                   "sex": "M",
                                                   "date_of_birth": "1980-10-01T00:00:00Z",
                                                   "place_of_birth": "New York",
                                                   "country": "USA"})
        self.assertEqual(user_informations.name, 'Tony')
        self.assertEqual(user_informations.surname, 'Stark')
        self.assertEqual(user_informations.sex, 'M')
        self.assertEqual(user_informations.date_of_birth, datetime.datetime(1980, 10, 1, 0, 0))
        self.assertEqual(user_informations.place_of_birth, 'New York')
        self.assertEqual(user_informations.country, 'USA')
