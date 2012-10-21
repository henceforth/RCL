import pygame
import logging
import time
import os
import pydoc

from CallbackObject import FunctionCallObject

logging.basicConfig(level=logging.DEBUG, filename="logs/Display.log")
#logging.basicConfig(level=logging.DEBUG)

class Display(object):
    '''Basic Display class
    used by windows to register themselves
    each window's suface is gotten when update() is called
    '''
    logger = None
    windowList = []

    def __init__(self):
        self.logger = logging.getLogger("display")
        self.logger.debug("starting")

        if pygame.display.get_init() == False:
            self.logger.info("starting pygame")
            pygame.display.init()
            pygame.display.set_mode()
            #todo: fenstergroesse speichern und an fenster verteilen
            self.logger.info("driver: %s" % pygame.display.get_driver())

    def __del__(self):
        pass
        #todo: kill windows

    def registerWindow(self, window):
        '''Args: Window instance
        will add the window to the list of windows to refresh
        '''
        self.windowList.append(window)
        self.logger.debug("register window #%i" % window.wId)

    def update(self):
        '''called once per tick, to update all registered window'''
        #self.logger.debug("updating %i windows" % len(self.windowList))
        posy = 0
        for n in self.windowList:
            pygame.display.get_surface().blit(n.draw(), (0, posy))
            posy += n.h

        pygame.display.flip()


windowCount = 0
class Window(object):
    '''abstract base class for a Window
    user needs to override the render and add methods
    '''
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

        self.winSurface = pygame.Surface((self.w, self.h))

        self.logger = logging.getLogger("window%i" % self.wId)
        self.logger.debug("starting")

    def __del__(self):
        self.logger.debug("killed")

    def clear(self):
        '''resets the window's surface the line counter
        '''
        self.logger.debug("clearing")
        self.winSurface = pygame.Surface((self.w, self.h))
        self.currentLine = 0
        self.dirty = True
    
    def draw(self):
        '''
        refreshes the surface if the window is dirty
        '''
        #self.logger.debug("drawing")
        if self.dirty:
            self.render()

        return self.winSurface

    def render(self):
        '''must be implemented
        provides a way to get the content from self.entries
        and puts them onto the window's surface
        '''
        #blit on surface, then set clean
        raise NotImplemented("Window::Render")
    
    def add(self, element):
        '''
        registers content for the window and puts
        the content to self.entries
        '''
        #add content like lines or pictures
        #encapsulation of adding content
        raise NotImplemented("Window::Add")
    
    def __iadd__(self, *element):
        '''parameter overload to provide += (append) functionality
        '''
        self.add(*element)

    def __lshift__(self, *element):
        '''parameter overload to provide << (reset and set) functionality
        '''
        self.clear()
        self.add(*element)

class PictureWindow(Window):
    '''window implementation that loads a picture
    may be loaded from disk by file name or 
    fom buffer by providing StringIO instace'''

    fileName = None

    def __init__(self, h=300, w=1600):
        super(PictureWindow, self).__init__(h, w)
        self.logger.debug("picture window starting up")

    def add(self, *args):
        self.loadPicture(*args)

    def loadPicture(self, filename):
        '''set picture internally
        argument may be string (file is loaded from disk) or
        buffer (file is loaded from that buffer'''
        #loads string and buffer
        self.fileName = filename
        self.dirty = True

    def render(self):
        if self.dirty:
            self.clear()
            self.logger.debug("attempting to load %s" % self.fileName)
            image = pygame.image.load(self.fileName)
            self.winSurface.blit(image, pygame.Rect(0, 0, 100, 100))
            self.dirty = False


class TextWindow(Window):
    '''window implementation that can display lines of text
    '''
    fontName = None
    font = None
    currentLine = None
    fontSize = 20 

    def __init__(self, h=300, w=1600):
        super(TextWindow, self).__init__(h, w)
        self.logger.debug("textwindow, initing pygame font")
        pygame.font.init()

        self.fontName = "lat1-16.psfu.gz"
        self.font = pygame.font.SysFont(self.fontName, self.fontSize)
        self.logger.info("font found: %s"% self.font)

        self.currentLine = 0
        self.entries = []

        self.logger.debug("created textwindow, w: %i, h: %i, font: %s, surface: %s" % (self.w, self.h, self.fontName, self.winSurface))

    def add(self, textToRender):
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

    def __lshift__(self, element):
        self.deleteLines()
        self.add(element)

    def deleteLines(self):
        self.currentLine = 0
        self.entries = []
        self.dirty = True
        self.clear()


class TextMenuWindow(TextWindow):
    '''window implementation that loads text 
    and provides possibility to set function hook for each line
    so lines can be selected like a menu
    '''
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
            self.dirty = False
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
        self.dirty = False

    def add(*args):
        self.registerEntry(*args)

    def registerEntry(self, entryText, functionToCall, *argumentList):
        '''
        registers a text line, a function to call and its arguments
        when the line is selected and select() is called
        the function provided will be called and the argumentList
        is passed to it
        '''
        #making sure the cursor is set as soon
        #as there is something to set it on
        if self.currentPosition == -1:
            self.currentPosition = 0

        #check if hook gets re-registered
        isIn = False
        for savedEntry in self.entries:
            if entryText == savedEntry.keys()[0]:
                isIn = True

        if isIn:
            #entryText is saved and new functionHook will be appended
            for n in self.entries:
                eName = n.keys()[0]
                fCallList = n.values()[0]
                if entryText == eName:
                    fCallList.append(FunctionCallObject(functionToCall, *argumentList))
                    self.logger.debug("now %i callbacks for %s" % (len(fCallList), eName))
        else:
            #entryText is new
            if len(argumentList) == 0:
                self.logger.debug("registering callback without args")
                self.entries.append({entryText: [FunctionCallObject(functionToCall)]})
            else:
                self.logger.debug("registering callback with %i args", len(argumentList))
                self.entries.append({entryText: [FunctionCallObject(functionToCall, *argumentList)]})
            #only dirty when a new new line was added
            self.dirty = True


    def moveUp(self):
        self.logger.debug("moving up")
        if self.currentPosition <= 0:
            return
        else:
            self.dirty = True
            self.currentPosition -= 1

    def moveDown(self):
        self.logger.debug("moving down")
        if self.currentPosition >= len(self.entries)-1:
            return
        else:
            self.dirty = True
            self.currentPosition += 1

    def select(self):
        self.logger.debug("selected")
        functionToCallList = self.entries[self.currentPosition].values()[0]
        for functionToCall in functionToCallList:
            self.logger.debug("calling %s" % functionToCall)
            functionToCall()

def dummyFunc():
    print "dummyFunc called"

def dummyFunc2():
    print "dummyFunc2 called"

def dummyFunc3(*args):
    if len(args) > 0:
        print "dummyFunc3 called, list of arguments: %s" % [args]
    else:
        print "dummyFunc3 without arguments called"

if __name__=="__main__":
    logger = logging.getLogger("test")

    d1 = Display()
    d1.update()#without any windows
    logger.debug("sleeping")
    time.sleep(1)

    statusWindow = TextWindow(25, 1600)
    tw1 = TextWindow(50, 1600)
    tmw1 = TextMenuWindow(150, 1600)
    pw1 = PictureWindow(500, 1600)

    d1.registerWindow(statusWindow)
    statusWindow << "one window without content"
    d1.registerWindow(tw1)
    d1.update()#with one window without content
    logger.debug("sleeping")
    time.sleep(1)

    statusWindow << "one window, 2 items"
    tw1 << "hello world"
    tw1 += "hello world, again"
    d1.update()#one window, 2 lines
    logger.debug("sleeping")
    time.sleep(1)

    statusWindow << "starting picture window"
    d1.registerWindow(pw1)
    pw1 << "one.jpg"
    d1.update()
    logger.debug("sleeping")
    time.sleep(1)

    statusWindow << "two window, 2 entries each, picture window"

    tmw1.registerEntry("line1", dummyFunc)
    tmw1.registerEntry("line2", dummyFunc2)
    tmw1.registerEntry("line3", dummyFunc3)
    tmw1.registerEntry("line4", dummyFunc3, 1, 2, 3, None)
    tmw1.registerEntry("line4", dummyFunc3, [1, 2, 3, None])
    tmw1.registerEntry("line4", dummyFunc3, [1, 2], [3, None])
    tmw1.registerEntry("line4", dummyFunc3, [1, 2, 3, [1, 2, 3]])

    d1.registerWindow(tmw1)
    d1.update()#two windows, 2 entries each
    logger.debug("sleeping")
    time.sleep(1)

    statusWindow << "selector moved down"

    tmw1.moveDown()
    d1.update()#entry below selected
    tmw1.select()#dummyfunc1
    logger.debug("sleeping")
    time.sleep(1)

    statusWindow << "selector moved up"

    tmw1.moveUp()
    d1.update()#entry above sected
    logger.debug("sleeping")
    time.sleep(1)

    statusWindow << "4 times move down and select w/o rendering"

    tmw1.select()
    tmw1.moveDown()
    tmw1.select()
    tmw1.moveDown()
    tmw1.select()
    tmw1.moveDown()
    tmw1.select()
    tmw1.moveDown()

    d1.update()#4 times moved down
    logger.debug("sleeping")
    time.sleep(1)
