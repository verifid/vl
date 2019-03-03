#!/usr/bin/python

import connexion

app = connexion.App(__name__, specification_dir='./swagger/')
