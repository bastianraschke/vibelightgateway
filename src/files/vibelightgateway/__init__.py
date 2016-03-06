#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
VibeLight Gateway
Copyright (C) 2016 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

@author: Bastian Raschke <bastian.raschke@posteo.de>
"""

import threading

__version__ = '1.0'


class BaseModule(threading.Thread):
    """
    VibeLight base module.
    Important: All VibeLight modules must inherit from this base class!

    """

    def __init__(self, requestData, neopixelStrip):

        threading.Thread.__init__(self)
        self.__isInterrupted = False
        
        self._requestData = requestData
        self._neopixelStrip = neopixelStrip

    def isInterrupted(self):
        return self.__isInterrupted

    def interrupt(self):
        self.__isInterrupted = True

    def run(self):
        raise NotImplementedError('The method run() must be implemented by module!')
