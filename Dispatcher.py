import logging
import pygame
import pydoc

from CallbackObject import FunctionCallObject

class Dispatcher(object):
    '''base class to support distributing of messages
    after checking for an event in a queue based on implementation
    '''
    logger = None
    entries = None

    def __init__(self):
        self.logger = logging.getLogger("dispatcher")
        self.logger.debug("start")
        self.entries = []

    def getCallback(self, key):
        '''returns a list of callbacks for each key
        list order is register order
        '''
        self.logger.debug("looking up key: %s" % key)
        for n in self.entries:
            if key in n.keys():
                self.logger.debug("found callback for %s" % key)
                return n[key]

        return None

    def check(self):
        '''needs to be implented by derivate
        gets called by the main process to check the queue and call events
        '''
        #responsible to call methods for incoming events
        raise NotImplemented("InputDispatcher::check")

    def register(self, key, functionToCall):
        '''registers a function and an event type
        the function is called once the event type is detected
        '''
        if self.getCallback(key) != None:
            self.getCallback(key).append(functionToCall)
        else:
            #create new entry
            self.entries.append({key: [FunctionCallObject(functionToCall)]})

class PyGameEventDispatcher(Dispatcher):
    '''dericate of EventDispatcher for checking
    the pygame event queue for keyboard events
    '''

    def __init__(self):
        super(PyGameEventDispatcher, self).__init__()
        self.logger.debug("pygame dispatcher start")

    def check(self):
        events = pygame.event.get()
        for curEvent in events:
            self.logger.debug("got event: %s" % (curEvent))
            if curEvent.type == pygame.KEYDOWN:
                funcToCallList = self.getCallback(curEvent.key)
                if funcToCallList != None:
                    self.logger.debug("calling callback for %s" % curEvent.key)
                    for n in funcToCallList:
                        n()

