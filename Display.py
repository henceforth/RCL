import pygame
import logging
import time

#logging.basicConfig(level=logging.DEBUG, filname="logs/Display.log")

class Display(object):
    logger = None
    windowList = []

    def __init__(self):
        self.logger = logging.getLogger("display")
        self.logger.debug("starting")

        if pygame.display.get_init() == False:
            self.logger.info("starting pygame")
            pygame.display.init()
            pygame.display.set_mode()
            self.logger.info("driver: %s" % pygame.display.get_driver())

    def __del__(self):
        pass
        #todo: kill windows

    def registerWindow(self, window):
        self.windowList.append(window)
        self.logger.debug("register window #%i" % window.wId)

    def update(self):
        self.logger.debug("updating %i windows" % len(self.windowList))
        posy = 0
        for n in self.windowList:
            pygame.display.get_surface().blit(n.draw(), (0, posy))
            posy += n.h

        pygame.display.flip()


windowCount = 0
class Window(object):
    wId = -1
    w = 0
    h = 0
    winSurface = None

    def __init__(self):
        global windowCount
        self.wId = windowCount
        windowCount += 1

        self.logger = logging.getLogger("window%i" % self.wId)
        self.logger.debug("starting")

    def __del__(self):
        self.logger.debug("killed")

    def draw(self):
        #implementation must provide draw function
        #return surface
        raise NotImplemented("Window::Draw")

    def clear(self):
        #reallocates the surface
        raise NotImplemented("Window::Clear")

class TextWindow(Window):
    fontName = None
    font = None
    currentLine = None
    fontSize = 24 

    def __init__(self):
        super(TextWindow, self).__init__()
        self.logger.debug("textwindow, initing pygame font")
        pygame.font.init()

        self.fontName = "lat1-16.psfu.gz"
        self.font = pygame.font.SysFont(self.fontName, self.fontSize)
        self.logger.info("font found: %s"% self.font)

        self.currentLine = 0
        self.w = 1600
        self.h = 800

        self.winSurface = pygame.Surface((self.w, self.h))
        self.logger.debug("created textwindow, w: %i, h: %i, font: %s, surface: %s" % (self.w, self.h, self.fontName, self.winSurface))

    def render(self, textToRender):
        self.logger.debug("rendering text: %s" % textToRender)
        surf = self.font.render(textToRender, True, (255, 255, 255), (0, 0, 0))
        self.winSurface.blit(surf, (0, self.currentLine*16))
        self.currentLine += 1

    def clear(self):
        self.logger.debug("clearing")
        self.winSurface = pygame.Surface((self.w, self.h))
        self.currentLine = 0
    
    def draw(self):
        self.logger.debug("drawing")
        retSurface = self.winSurface
        self.clear()
        return retSurface

class TextMenu(object):
    debugger = None

    def __init__(self):
        self.debugger = logging.getLogger("textMenu")


class TextWindowFormatter(object):
    logger = None

    def __init__(self):
        self.logger = logging.getLogger("TextWindowFormatter")


if __name__=="__main__":
    d1 = Display()
    w1 = Window() #abstract
    tw1 = TextWindow()
    tw2 = TextWindow()

    d1.registerWindow(tw1)
    d1.registerWindow(tw2)
    

    tw1.render("hello world!")
    tw2.render("bye world!")
    d1.update()
    time.sleep(10)
