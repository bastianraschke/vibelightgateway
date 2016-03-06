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
import time

from vibelightgateway import BaseModule
from vibelightgateway.neopixeleffects import switchAllToColor


## Get main log instance
logger = logging.getLogger('vibelightgateway')

RAINBOW_WAIT = 20

class rainbow(BaseModule):
    """
    VibeLight module that allows to show a rainbow with the LEDs.

    """

    def rainbowWheel(self, position):
        """
        Generate rainbow colors across 0-255 positions.

        """

        if (position < 85):
            return neopixel.Color(position * 3, 255 - position * 3, 0)
        elif (position < 170):
            position -= 85
            return neopixel.Color(255 - position * 3, 0, position * 3)
        else:
            position -= 170
            return neopixel.Color(0, position * 3, 255 - position * 3)

    def run(self):

        try:
            requestCommand = self._requestData['command']

            if ( requestCommand == 'start' ):

                while ( self.isInterrupted() == False ):

                    for j in range(256):

                        for i in range(self._neopixelStrip.numPixels()):
                            self._neopixelStrip.setPixelColor(i, self.rainbowWheel((i+j) & 255))
                        self._neopixelStrip.show()

                        ## In-loop check if we are still interrupted to minimize delay
                        if ( self.isInterrupted() == True ):
                            break

                        time.sleep(RAINBOW_WAIT / 1000.0)

            else:
                ## Switch all pixels off
                switchAllToColor(self._neopixelStrip, neopixel.Color(0, 0, 0))

        except:
            logger.error('Unexpected error occured:', exc_info=1)




