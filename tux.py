#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tuxisalive.api import *
import sys
import time
import random

import feedparser

TUX_SERVER = '127.0.0.1'
TUX_PORT = 270

class TuxTouchFlippers:
    def __init__(self, tux=None):
        self.tux = tux
        self.registerWhenTouchFlippers()
    def registerWhenTouchFlippers(self):
        self.tux.button.right.registerEventOnPressed(self.onPressed)
        self.tux.button.left.registerEventOnPressed(self.onPressed)
    def onPressed(self, value1, value2):
        self.tux.eyes.onAsync(1, SSV_OPEN)

class TuxRemote:
    def __init__(self, tux=None):
        self.tux = tux
        remote = self.tux.button.remote
        actions = [
            {'event' : K_RED, 'action': self.getChuckNorrisFact},
            {'event' : K_GREEN, 'action' : self.dance},
#            {'event' : K_BLUE, 'action' : self.hello},
#            {'event' : K_YELLOW, 'action' : self.bye},
            {'event' : K_1, 'action' : self.winkRight},
            {'event' : K_2, 'action' : self.winkLeft},
            {'event' : K_3, 'action' : self.rotateLeft},
            {'event' : K_4, 'action' : self.rotateRight}
        ]
        for action in actions:
            remote.registerEventOnPressed(action['action'], action['event'])

    def getChuckNorrisFact(self, value1, value2):
        print "chuck norris"
        feed = feedparser.parse("http://www.chucknorrisfacts.fr/xml/facts.xml")
        entry = random.choice(feed['entries'])
        print entry['description']
        self.tux.tts.speakAsync(str(entry['description'].encode('utf-8').replace('Chuck Norris', 'TcheuK Norisse')))

    def dance(self, value1, value2):
        print "dance"
        self.tux.flippers.onAsync(3, SSV_DOWN, SPV_NORMAL)

    def hello(self, value1, value2):
        self.tux.flippers.on(3, SSV_DOWN, SPV_NORMAL)
        self.tux.mouth.open()
        self.tux.tts.speak("Bonjour !")
        self.tux.mouth.close()

    def bye(self, value1, value2):
        self.tux.flippers.on(3, SSV_DOWN, SPV_NORMAL)
        self.tux.mouth.open()
        self.tux.tts.speak("Au revoir !")
        self.tux.mouth.close()
 
    def winkRight(self, value1, value2):
        self.tux.led.right.blinkDuring(SPV_FAST, 0.5)
        self.tux.led.right.on()

    def winkLeft(self, value1, value2):
        self.tux.led.left.blinkDuring(SPV_FAST, 0.5)
        self.tux.led.left.on()
    
    def rotateLeft(self, value1, value2):
        print "rotate left"
        self.tux.spinning.leftOn(1.0)

    def rotateRight(self, value1, value2):
        print "rotate right"
        self.tux.spinning.rightOn(1.0)
        
    
if __name__ == "__main__":
    tux = TuxAPI(TUX_SERVER, TUX_PORT)
    tux.server.autoConnect(CLIENT_LEVEL_RESTRICTED, 'MyAppName2', 'myPassword')
    tux.server.waitConnected(10.0)
    if tux.server.getConnected():
        print "Wait dongle connected (10 seconds )..."
        tux.dongle.waitConnected(10.0)
        print "Dongle connected :", tux.dongle.getConnected()
        if tux.dongle.getConnected():
            print "ready"
            tux.tts.setEncoding("utf-8")
            tux.tts.setLocutor("Julie")
            TuxTouchFlippers(tux)
            TuxRemote(tux)
            try:
		while 1:
                    time.sleep(10)
            except KeyboardInterrupt:
		print '\nINTERUPT'
		sys.exit(1)
        else:
            print "dongle not connected"
    else:
        print "not connected"
    tux.destroy()
    print "end"

