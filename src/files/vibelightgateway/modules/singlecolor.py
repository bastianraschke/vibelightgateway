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

from vibelightgateway import BaseModule
from vibelightgateway.neopixeleffects import switchAllToColor


## Get main log instance
logger = logging.getLogger('vibelightgateway')

class singlecolor(BaseModule):
    """
    VibeLight module that allows to set the LEDs to one static color.

    """

    def run(self):

        try:
            colorRed = self._requestData['r']
            colorGreen = self._requestData['g']
            colorBlue = self._requestData['b']

            ## Validate if the received data are valid colors:
            if ( colorRed < 0 or colorRed > 255 ): raise ValueError('The received color (R) is invalid!')
            if ( colorGreen < 0 or colorGreen > 255 ): raise ValueError('The received color (G) is invalid!')
            if ( colorBlue < 0 or colorBlue > 255 ): raise ValueError('The received color (B) is invalid!')

            logger.info('Setting color to: ' + str((colorRed, colorGreen, colorBlue)))

            ## Set the complete LED strip to one color
            switchAllToColor(self._neopixelStrip, neopixel.Color(colorRed, colorGreen, colorBlue))

        except:
            logger.error('Unexpected error occured:', exc_info=1)
