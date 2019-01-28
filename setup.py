# !/usr/bin/env python
from setuptools import setup
from setuptools import find_packages

setup(
    name='max gas',
    packages=find_packages(exclude=['tests*', 'docs']),
    version='0.1.0',
    description='bode miller',
    install_requires=['Django', 'djangorestframework']
)
