#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirementstxt = f.read().splitlines()

setup(
    name='gitbuglink',
    version='0.0.2',
    description='The stupid commit-bug traceability linker for the stupid content tracker',
    long_description=readme,
    author='Christopher S. Corley',
    author_email='cscorley@crimson.ua.edu',
    url='https://github.com/cscorley/gitbuglink',
    license=license,
    packages=['gitbuglink'],
    keywords = [],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Version Control",
        "Topic :: Text Processing",
        ],
    py_modules=['gitbuglink'],
    install_requires=requirementstxt,
    entry_points='''
        [console_scripts]
        gitbuglink=gitbuglink:gitbuglink.main
    ''',
)
