import logging
import pygame

class InputDispatcher(object):
    logger = None

    def __init__(self):
        self.logger = logging.getLogger("dispatcher")
        self.logger.debug("start")

    def check(self):
        #responsible to call methods for incoming events
        raise NotImplemented("InputDispatcher::check")

class PyGameEventDispatcher(InputDispatcher):

    def __init__(self):
        super(PyGameEventDispatcher, self).__init__()
        self.logger.debug("pygame dispatcher start")

    def check(self):
        curEvent = pygame.event.poll()
        while curEvent.type != pygame.NOEVENT:
            self.logger.debug ("got event: %s" % (curEvent))
            if curEvent.type == pygame.KEYDOWN:
                if curEvent.key == pygame.K_q:
                    quit()

            curEvent = pygame.event.poll()
