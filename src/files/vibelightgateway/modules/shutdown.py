#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
VibeLight Gateway
Copyright (C) 2016 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

@author: Bastian Raschke <bastian.raschke@posteo.de>
"""

import commands
import logging
import neopixel
import time

from vibelightgateway import BaseModule
from vibelightgateway.neopixeleffects import switchAllToColor, slideFromRight, pulseBrightness


## Get main log instance
logger = logging.getLogger('vibelightgateway')

class shutdown(BaseModule):
    """
    VibeLight module that allows to shutdown the system.

    """

    def run(self):

        try:
            colorWhite = neopixel.Color(255, 255, 255)
            colorBlack = neopixel.Color(0, 0, 0)

            ## Shutdown animation
            pulseBrightness(self._neopixelStrip, 255, 0)
            slideFromRight(self._neopixelStrip, colorBlack)

            logger.info('Shutdown system...')
            commandStatus, commandOutput = commands.getstatusoutput('shutdown now -h')

            if ( commandStatus != 0 ):
                raise Exception('Shutdown failed: ' + str(commandOutput))

        except:
            logger.error('Unexpected error occured:', exc_info=1)
