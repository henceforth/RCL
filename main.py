import logging
logging.basicConfig(level=logging.INFO, filename="logs/main.log")
logging.captureWarnings(True)

import urllib2
import time
import pygame
import StringIO

import Parser
import Storage
import Display
import Dispatcher

import pydoc

#logging.basicConfig(level=logging.DEBUG, filename="logs/main.log")

class Runner(object):
    '''runner class to glue scraping, parsing and displaying together'''
    sleepTime = 0.05
    rescrapeTime = 30
    logger = None

    storage = None #link to reddit storage

    def __init__(self):
        self.logger = logging.getLogger("runner")

    def openLink(self, redditPostId, windowHandle):
        #self.logger.info("calling reddit post: %s" % redditPostId)
        redditPost = self.storage.get(redditPostId)
        self.logger.info("calling %s" % redditPost["url"])
        if redditPost["url"].split(".")[-1] in ("jpg", "gif", "png", "bmp", "tif"):
            request = urllib2.Request(redditPost["url"])
            request.add_header("User-agent", "have no fear, rscrape by /u/hcf is here")
            response = urllib2.urlopen(request)
            pictureToRender = StringIO.StringIO(response.read())
            windowHandle.add(pictureToRender)
        else:
            self.logger.info("not an image")


    def run(self):
        pygameEventDispatcher = Dispatcher.PyGameEventDispatcher()
        #redditParser = Parser.Parser("http://www.reddit.com/.json")
        redditParser = Parser.Parser("http://www.reddit.com/domain/i.imgur.com/.json")
        redditStorage = Storage.RedditStorage("reddit.db")
        self.storage = redditStorage #hax

        display = Display.Display()
        tw1 = Display.TextWindow(16, 1280)
        tmw1 = Display.TextMenuWindow(425, 1280)
        pw1 = Display.PictureWindow(800, 1280)

        display.registerWindow(tw1)
        display.registerWindow(tmw1)
        display.registerWindow(pw1)

        pygameEventDispatcher.register(pygame.K_UP, tmw1.moveUp)
        pygameEventDispatcher.register(pygame.K_UP, tmw1.select)
        pygameEventDispatcher.register(pygame.K_DOWN, tmw1.moveDown)
        pygameEventDispatcher.register(pygame.K_DOWN, tmw1.select)
        pygameEventDispatcher.register(pygame.K_RETURN, tmw1.select)

        pw1.add("one.jpg")

        run = True
        lastRedditUpdate = 0
        data = None
        dirty = False
        while run:
            #get reddit content
            if time.time() - lastRedditUpdate > self.rescrapeTime:
                self.logger.debug("getting reddit content")
                data = redditParser.getContent()
                #store entries
                self.logger.debug("saving content")
                redditStorage.store(data)
                #store update time
                #lastRedditUpdate = data.keys()[0]
                lastRedditUpdate = time.time()
                dirty = True #todo: dirty nur wenn storage neu eintaege meldet

            #display entries
            if dirty:
                #status window
                self.logger.debug("updating status window")
                tw1 << "last update: %s" % time.strftime("%c", time.localtime(lastRedditUpdate))

                self.logger.debug("rendering content")
                tmw1.deleteLines()
                for n in data[data.keys()[0]]:
                    tmw1.registerEntry("%s by %s" % (n["data"]["title"], n["data"]["author"]), self.openLink , n["data"]["id"], pw1)

                self.logger.debug("display content")
                dirty = False
            display.update()

            #render selected in contentWindow
            #save displayed entries

            #self.logger.info("dispatching")
            pygameEventDispatcher.check()

            #self.logger.info("sleeping for %f seconds" % self.sleepTime)
            time.sleep(self.sleepTime)

        self.logger.info("shutting down...")

def dummy():
    print "dummy"

if __name__ == "__main__":
    r1 = Runner()
    r1.run()
