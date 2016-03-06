#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
VibeLight Gateway
Copyright (C) 2016 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

@author: Bastian Raschke <bastian.raschke@posteo.de>
"""

import neopixel
import time


def switchAllToColor(neopixelStrip, color):

    for i in range(neopixelStrip.numPixels()):
        neopixelStrip.setPixelColor(i, color)

    neopixelStrip.show()

def slideFromLeft(neopixelStrip, color):

    for i in range(neopixelStrip.numPixels()):
        neopixelStrip.setPixelColor(i, color)
        neopixelStrip.show()
        time.sleep(0.009)

def slideFromRight(neopixelStrip, color):

    for i in range(neopixelStrip.numPixels(), -1, -1):
        neopixelStrip.setPixelColor(i, color)
        neopixelStrip.show()
        time.sleep(0.009)

def pulseBrightness(neopixelStrip, brightnessStart, brightnessEnd):

    if ( brightnessStart < 0 or brightnessStart > 255 ):
        raise ValueError('The given brightnessStart is invalid!')

    if ( brightnessEnd < 0 or brightnessEnd > 255 ):
        raise ValueError('The given brightnessEnd is invalid!')

    for currentBrightness in range(brightnessStart, brightnessEnd, -1):

        for i in range(neopixelStrip.numPixels()):
            neopixelStrip.setPixelColor(i, neopixel.Color(currentBrightness, currentBrightness, currentBrightness))
        neopixelStrip.show()

        time.sleep(0.00001)

    for currentBrightness in range(brightnessEnd, brightnessStart):

        for i in range(neopixelStrip.numPixels()):
            neopixelStrip.setPixelColor(i, neopixel.Color(currentBrightness, currentBrightness, currentBrightness))
        neopixelStrip.show()

        time.sleep(0.00001)
