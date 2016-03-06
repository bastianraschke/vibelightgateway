#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
VibeLight Gateway
Copyright (C) 2016 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

@author: Bastian Raschke <bastian.raschke@posteo.de>
"""

import importlib
import json
import logging
import neopixel
import os
import signal
import sys
import time
import threading

from vibelightgateway.neopixeleffects import slideFromLeft, slideFromRight, pulseBrightness

from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol
from twisted.internet import reactor


"""
NeoPixel configuration

"""

## Number of LED pixels
LED_COUNT = 60

## GPIO pin connected to the pixels (must support PWM)
LED_PIN = 18

## LED signal frequency in hertz (usually 800 kHz)
LED_FREQ_HZ = 800000

## DMA channel to use for generating signal (try 5)
LED_DMA = 5

## LED brightness [0..255]
LED_BRIGHTNESS = 250

## True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False


"""
VibeLight Gateway configuration

"""

## Websocket server address
GATEWAY_ADDRESS = '127.0.0.1'

## Websocket server port
GATEWAY_PORT = 9000

## Enabled VibeLight modules
## Note: See in directory "/usr/lib/python2.7/dist-packages/vibelightgateway/modules/"" for available modules.
ENABLED_MODULES = [
    'singlecolor',
    'party',
    'rainbow',
    'shutdown',
]


"""
VibeLight Gateway server logic

"""

class VibeLightGatewayProtocol(WebSocketServerProtocol):
    """
    VibeLight protocol implementation.

    """

    def __handleRequest(self, requestData):

        global currentModuleInstance
        global currentModuleInstanceSemaphore

        global neopixelStrip

        responseStatus = 'OK'

        try:
            ## Try to parse the received JSON message
            parsedRequetData = json.loads(requestData)

            requestModule = parsedRequetData['module']
            requestPayload = parsedRequetData['payload']

            ## Execute requested module only if allowed
            if ( requestModule in ENABLED_MODULES ):

                with currentModuleInstanceSemaphore:

                    if (currentModuleInstance != None and currentModuleInstance.isInterrupted() == False):
                        currentModuleInstance.interrupt()
                        currentModuleInstance.join()
                        logger.debug('Stopped previous module thread.')

                    currentModuleClass = importlib.import_module('vibelightgateway.modules.' + requestModule)
                    currentModuleInstance = getattr(currentModuleClass, requestModule)(requestPayload, neopixelStrip)
                    currentModuleInstance.start()
            else:
                responseStatus = 'ERROR_INVALID_MODULE'

        except:
            responseStatus = 'ERROR_INVALID_REQUEST'
            logger.error('Unexpected error occured:', exc_info=1)

        return responseStatus

    def onConnect(self, request):
        logger.info('Client connecting: ' + str(request.peer))

    def onOpen(self):
        logger.info('Connection opened.')

    def onMessage(self, requestData, isBinary):
        logger.debug('Message received: ' + str(requestData))

        if ( isBinary == True ):
            responseStatus = 'ERROR_BINARY_REQUEST'
        else:
            responseStatus = self.__handleRequest(requestData)

        self.sendMessage(responseStatus, binary=False)

    def onClose(self, wasClean, code, reason):
        logger.info('Connection closed: ' + str(reason))

if ( __name__ == '__main__' ):

    ## Checks if user is root
    if ( os.geteuid() != 0 ):
        sys.stderr.write('Error: You need to have root privileges!\n')
        sys.exit(1)

    currentModuleInstance = None
    currentModuleInstanceSemaphore = threading.Semaphore(value=1)

    ## Initialize logger

    logger = logging.getLogger('vibelightgateway')
    logger.setLevel(logging.DEBUG)

    logFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(logFormatter)
    logger.addHandler(streamHandler)

    def KeyboardInterruptHandler(signal, frame):
        """
        Handler for IPC signals.

        """

        logger.info('Stopping websocket server...')

        with currentModuleInstanceSemaphore:

            if (currentModuleInstance != None and currentModuleInstance.isInterrupted() == False):
                currentModuleInstance.interrupt()
                currentModuleInstance.join()

        reactor.stop()

    ## Handle the CTRL+C signal to shutdown
    signal.signal(signal.SIGINT, KeyboardInterruptHandler)

    ## Create and initialize the NeoPixel library
    logger.info('Loading NeoPixel library...')
    neopixelStrip = neopixel.Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    neopixelStrip.begin()

    ## Startup animation

    colorWhite = neopixel.Color(255, 255, 255)
    colorBlack = neopixel.Color(0, 0, 0)

    slideFromLeft(neopixelStrip, colorWhite)
    slideFromRight(neopixelStrip, colorBlack)
    slideFromRight(neopixelStrip, colorWhite)

    pulseBrightness(neopixelStrip, 255, 10)

    logger.info('Starting websocket server...')

    factory = WebSocketServerFactory('ws://' + GATEWAY_ADDRESS + ':' + str(GATEWAY_PORT), debug=False)
    factory.protocol = VibeLightGatewayProtocol

    logger.info('Listening...')

    reactor.listenTCP(GATEWAY_PORT, factory)
    reactor.run()
