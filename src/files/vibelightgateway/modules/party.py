#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
VibeLight Gateway
Copyright (C) 2016 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

@author: Bastian Raschke <bastian.raschke@posteo.de>
"""

import logging
import neopixel
import random
import time

from vibelightgateway import BaseModule
from vibelightgateway.neopixeleffects import switchAllToColor


## Get main log instance
logger = logging.getLogger('vibelightgateway')

class party(BaseModule):
    """
    VibeLight module for partying.

    """

    def run(self):

        try:
            requestCommand = self._requestData['command']

            if ( requestCommand == 'start' ):

                requestEffectSpeed = int(self._requestData['speed'])

                if ( requestEffectSpeed < 60 or requestEffectSpeed > 200 ):
                    raise ValueError('The requested speed value is invalid!')

                while ( self.isInterrupted() == False ):

                    colorRed = random.randint(50, 255)
                    colorGreen = random.randint(50, 255)
                    colorBlue = random.randint(50, 255)

                    ## Set the complete LED strip to one color
                    switchAllToColor(self._neopixelStrip, neopixel.Color(colorRed, colorGreen, colorBlue))

                    ## Calculate BPM sleep
                    time.sleep(1.0 / (requestEffectSpeed / 60))

            else:
                ## Switch all pixels off
                switchAllToColor(self._neopixelStrip, neopixel.Color(0, 0, 0))

        except:
            logger.error('Unexpected error occured:', exc_info=1)




