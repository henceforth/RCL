import logging
#logging.basicConfig(level=logging.INFO, filename="logs/main.log")
logging.basicConfig(level=logging.DEBUG, filename="logs/main.log")
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
    run = True

    storage = None #link to reddit storage

    def __init__(self):
        self.logger = logging.getLogger("runner")

    def openLink(self, redditPostId, windowHandle):
        '''callback for loading reddit posts if accept is called in the text menu
        '''
        redditPost = self.storage.get(redditPostId)
        self.logger.debug("calling %s" % redditPost["url"])

        if redditPost["url"].split(".")[-1] in ("jpg", "gif", "png", "bmp", "tif"):
            pictureToRender = None
            if "xx-buffer" not in redditPost.keys():
                self.logger.info("downloading new image for post %s" % redditPostId)
                request = urllib2.Request(redditPost["url"])
                request.add_header("User-agent", "have no fear, rscrape by /u/hcf is here")
                response = urllib2.urlopen(request)
                redditPost["xx-buffer"] = response.read()
                self.storage.sync()
            else:
                self.logger.debug("loading picture from buffer")

            pictureToRender = StringIO.StringIO(redditPost["xx-buffer"])
            windowHandle.add(pictureToRender)
        else:
            self.logger.info("not an image")

    def stop(self):
        self.run = False


    def run(self):
        #setup parser
        pygameEventDispatcher = Dispatcher.PyGameEventDispatcher()
        #redditParser = Parser.Parser("http://www.reddit.com/.json")
        redditParser = Parser.Parser("http://www.reddit.com/domain/i.imgur.com/.json")
        redditStorage = Storage.RedditStorage("reddit.db")
        self.storage = redditStorage #hax

        #create display and window
        display = Display.Display()
        tw1 = Display.TextWindow(16, 1280)
        tmw1 = Display.TextMenuWindow(200, 1280)
        pw1 = Display.PictureWindow(800, 1280)

        #register windows
        #display.registerWindow(tw1)
        display.registerWindow(tmw1)
        display.registerWindow(pw1)

        #register callbacks
        pygameEventDispatcher.register(pygame.K_q, self.stop)
        pygameEventDispatcher.register(pygame.K_UP, tmw1.moveUp)
        pygameEventDispatcher.register(pygame.K_UP, tmw1.select)
        pygameEventDispatcher.register(pygame.K_DOWN, tmw1.moveDown)
        pygameEventDispatcher.register(pygame.K_DOWN, tmw1.select)
        pygameEventDispatcher.register(pygame.K_RETURN, tmw1.select)

        #time since last scrape
        lastRedditUpdate = 0
        #buffer to pass between scraper and storage
        data = None
        #flag for new entries
        dirty = True

        while self.run:
            #get reddit content
            if time.time() - lastRedditUpdate > self.rescrapeTime:
                self.logger.debug("getting reddit content")
                data = redditParser.getContent()
                #store entries
                self.logger.debug("saving content")
                new = redditStorage.store(data)
                #store update time
                #lastRedditUpdate = data.keys()[0]
                lastRedditUpdate = time.time()
                if new > 0:
                    self.logger.debug("found new entries, refresh")
                    dirty = True 

            #display entries
            if dirty:
                #status window
                self.logger.debug("updating status window")
                tw1 << "last update: %s" % time.strftime("%c", time.localtime(lastRedditUpdate))

                self.logger.debug("rendering content")
                tmw1.deleteLines()
                i = 0
                for n in data[data.keys()[0]]:
                    i += 1
                    title = n["data"]["title"]
                    author = n["data"]["author"]
                    postId = n["data"]["id"]
                    lineString =" %i - %s by %s" % (i, title, author)
                    tmw1.registerEntry(lineString, self.openLink, postId, pw1)

                self.logger.debug("display content")
                dirty = False
            display.update()

            #render selected in contentWindow
            #done by callbacks

            #save displayed entries

            #self.logger.info("dispatching")
            pygameEventDispatcher.check()

            #self.logger.info("sleeping for %f seconds" % self.sleepTime)
            time.sleep(self.sleepTime)

        pygame.quit()
        self.logger.info("shutting down...")

def dummy():
    print "dummy"

if __name__ == "__main__":
    r1 = Runner()
    r1.run()
