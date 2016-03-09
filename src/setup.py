#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
VibeLight Gateway
Copyright (C) 2016 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

@author: Bastian Raschke <bastian.raschke@posteo.de>
"""

from setuptools import setup, find_packages

import sys
sys.path.append('./files/')

## Dynamically get the module version
PACKAGE_VERSION = __import__('vibelightgateway').__version__

setup(
    name                = 'vibelightgateway',
    version             = PACKAGE_VERSION, ## Never forget to change Debian changelog file as well!
    description         = 'Ambiance light system (using WS2812B LED) for the Raspberry Pi.',
    author              = 'Bastian Raschke',
    author_email        = 'bastian.raschke@posteo.de',
    url                 = 'https://sicherheitskritisch.de',
    license             = 'D-FSL',
    packages            = find_packages(where='files'), ## Thanks to: http://www.siafoo.net/article/77
    package_dir         = {'': 'files'}
)
