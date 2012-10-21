import logging
import pygame
import pydoc

class InputDispatcher(object):
    '''base class to support distributing of messages'''
    logger = None
    entries = None

    def __init__(self):
        self.logger = logging.getLogger("dispatcher")
        self.logger.debug("start")
        self.entries = []

    def check(self):
        '''needs to be implented by derivate
        checks the event queue for input and calls the function if needed
        '''
        #responsible to call methods for incoming events
        raise NotImplemented("InputDispatcher::check")

    def register(self, key, functionToCall):
        '''registers a function and an event typei
        the function is called once the event type is detected
        '''
        self.entries.append({key: functionToCall})

class PyGameEventDispatcher(InputDispatcher):
    '''dericate of EventDispatcher for checking
    the pygame event queue for keyboard events
    '''

    def __init__(self):
        super(PyGameEventDispatcher, self).__init__()
        self.logger.debug("pygame dispatcher start")

    def check(self):
        curEvent = pygame.event.poll()
        while curEvent.type != pygame.NOEVENT:
            self.logger.debug("got event: %s" % (curEvent))
            if curEvent.type == pygame.KEYDOWN:
                if curEvent.key == pygame.K_q:
                    quit()

                for n in self.entries:
                    if curEvent.key == n.keys()[0]:
                        keys = n.keys()[0]
                        n[keys]()

            curEvent = pygame.event.poll()
