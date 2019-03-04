# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "vl"
VERSION = "1.0.0"

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="Identity Verification Layer",
    author_email="",
    url="",
    keywords=["Swagger", "Identity Verification Layer"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=__main__:main']},
    long_description="""\
    VerifID - Identity Verification Layer
    """
)

