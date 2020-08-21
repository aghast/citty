#!/usr/bin/env python3
# vim: fileencoding: utf-8
""" ROOT/setup.py

    Standard script to configure and invoke setuptools. This is used to create
    the package, bundle it for distribution on pypi, etc.

    This is *NOT* part of the deliverable; this is used to package up the
    deliverable.

"""
from setuptools import setup

setup(
    name="citty",
    entry_points={
        'console_scripts': [ 'citty = citty:main' ],
        'citty_test_funcs': [
            'make_test = citty:make_test',
        ],
    },
)
