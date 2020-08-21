#!/usr/bin/env python3
# vim: fileencoding: utf-8
""" ROOT/setup.py

    Standard script to configure and invoke setuptools. This is used to create
    the package, bundle it for distribution on pypi, etc.

    This is *NOT* part of the deliverable; this is used to package up the
    deliverable.

"""
from setuptools import setup

import citty

REPO_URL = "https://gitlab.com/aghast/citty/"

setup(
    author="aghast",
    author_email=chr(64).join(("aghast", "aghast\056" "dev")),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Testing",
    ],
    description=" ".join("""
        citty is CI for your TTY! It's a continuous-integration
        (CI) server that lives in a terminal (TTY) and displays
        colored text to indicate the status of different projects.

    """.strip().split()),
    entry_points={
        'console_scripts': [ 'citty = citty:main' ],
        'citty_test_funcs': [ 'make_test = citty:make_test', ],
    },
    keywords = """citty ci continuous integration terminal tty""",
    name="citty",
    url=REPO_URL,
    project_urls={
        "Documentation": REPO_URL + "-/blob/master/README.md#name",
        "Source Code": REPO_URL,
    },
    py_modules=[ "citty", ],
    version=citty.__version__,
)
