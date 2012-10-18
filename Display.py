import pygame
import logging
import time

#logging.basicConfig(level=logging.DEBUG, filname="logs/Display.log")
logging.basicConfig(level=logging.DEBUG)

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
    dirty = False

    def __init__(self, h, w):
        global windowCount
        self.wId = windowCount
        windowCount += 1

        self.h = h
        self.w = w

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
    #entries = None

    def __init__(self, h=300, w=1600):
        super(TextWindow, self).__init__(h, w)
        self.logger.debug("textwindow, initing pygame font")
        pygame.font.init()

        self.fontName = "lat1-16.psfu.gz"
        self.font = pygame.font.SysFont(self.fontName, self.fontSize)
        self.logger.info("font found: %s"% self.font)

        self.currentLine = 0
        self.entries = []

        self.winSurface = pygame.Surface((self.w, self.h))
        self.logger.debug("created textwindow, w: %i, h: %i, font: %s, surface: %s" % (self.w, self.h, self.fontName, self.winSurface))

    def addLine(self, textToRender):
        self.logger.debug("adding new text and rendering")
        self.entries.append(textToRender)
        self.dirty = True

    def render(self):
        #only to be called internally
        if not self.dirty:
            self.logger.debug("not dirty")
            return

        if len(self.entries) <= 0:
            self.logger.debug("nothing to render")
            return

        self.logger.debug("rendering %i entries" % len(self.entries))
        for textToRender in self.entries:
            self.logger.debug("rendering text: %s" % textToRender)
            surf = self.font.render(textToRender, True, (255, 255, 255), (0, 0, 0))
            self.winSurface.blit(surf, (0, self.currentLine*self.fontSize))
            self.currentLine += 1
        
        self.dirty = False

    def deleteLines(self):
        self.currentLine = 0
        self.entries = []
        self.dirty = True
        self.clear()

    def clear(self):
        self.logger.debug("clearing")
        self.winSurface = pygame.Surface((self.w, self.h))
        self.currentLine = 0
        self.dirty = True
    
    def draw(self):
        #self.logger.debug("drawing")
        if self.dirty:
            self.render()

        return self.winSurface

class TextMenuWindow(TextWindow):
    currentPosition = -1

    def __init__(self, h=300, w=1600):
        super(TextMenuWindow, self).__init__(h, w)
        self.logger.debug("textmenuwindow")

    def addLine(self, data):
        raise Exception("dont call this method on TextMenuWindow")

    def render(self):
        #only to be called internally
        if len(self.entries) <= 0:
            self.logger.debug("nothing to render")
            return
        
        currentLine = 0
        for entryToRender in self.entries:
            self.logger.debug("rendering menu entry: %s" % entryToRender)
            if self.entries[self.currentPosition] == entryToRender:
                #highlight selected entry
                surf = self.font.render(entryToRender.keys()[0], True, (255, 0, 0), (0, 0, 0))
            else:
                surf = self.font.render(entryToRender.keys()[0], True, (255, 255, 255), (0, 0, 0))
            
            currentLine += 1
            self.winSurface.blit(surf, (0, currentLine*self.fontSize))

    def registerEntry(self, entryText, functionToCall):
        #making sure the cursor is set as soon
        #as there is something to set it on
        if self.currentPosition == -1:
            self.currentPosition = 0

        self.logger.debug("registering %s" % entryText)
        self.entries.append({entryText: functionToCall})
        self.render()

    def moveUp(self):
        self.logger.info("moving up")
        if self.currentPosition <= 0:
            return
        else:
            self.dirty = True
            self.currentPosition -= 1

    def moveDown(self):
        self.logger.info("moving down")
        if self.currentPosition >= len(self.entries)-1:
            return
        else:
            self.dirty = True
            self.currentPosition += 1

    def select(self):
        self.logger.info("selected")
        self.entries[self.currentPosition].values()[0]()

def dummyFunc():
    print "dummyFunc called"

def dummyFunc2():
    print "dummyFunc2 called"

if __name__=="__main__":
    d1 = Display()
    d1.update()#without any windows
    time.sleep(1)

    statusWindow = TextWindow()
    tw1 = TextWindow()
    tmw1 = TextMenuWindow()

    d1.registerWindow(statusWindow)
    statusWindow.addLine("one window without content")

    d1.registerWindow(tw1)
    d1.update()#with one window without content
    time.sleep(1)

    statusWindow.deleteLines()
    statusWindow.addLine("one window, 2 items")

    tw1.addLine("hello world")
    tw1.addLine("hello world, again")
    d1.update()#one window, 2 lines
    time.sleep(1)

    statusWindow.deleteLines()
    statusWindow.addLine("two windows, 2 entries each")

    tmw1.registerEntry("line1", dummyFunc)
    tmw1.registerEntry("line2", dummyFunc2)
    tmw1.registerEntry("line3", dummyFunc)
    tmw1.registerEntry("line4", dummyFunc)

    d1.registerWindow(tmw1)
    d1.update()#two windows, 2 entries each
    time.sleep(1)

    statusWindow.deleteLines()
    statusWindow.addLine("selector moved down")

    tmw1.moveDown()
    d1.update()#entry below selected
    tmw1.select()#dummyfunc1
    time.sleep(1)

    statusWindow.deleteLines()
    statusWindow.addLine("selector moved up")

    tmw1.moveUp()
    d1.update()#entry above sected
    time.sleep(1)

    statusWindow.deleteLines()
    statusWindow.addLine("4 times moved down")
    tmw1.moveDown()
    tmw1.moveDown()
    tmw1.moveDown()
    tmw1.moveDown()

    d1.update()#4 times moved down
    time.sleep(1)

    d1.update()
    time.sleep(1)
