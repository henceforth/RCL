import logging
import Parser
import Storage
import time
import Display
import Dispatcher
import pygame
#logging.basicConfig(level=logging.DEBUG, filename="logs/main.log")
logging.basicConfig(level=logging.INFO)
logging.captureWarnings(True)

class Runner(object):
    sleepTime = 0.05
    rescrapeTime = 30
    windowRefreshTime = 5
    logger = None

    def __init__(self):
        self.logger = logging.getLogger("runner")


    def run(self):
        pygameEventDispatcher = Dispatcher.PyGameEventDispatcher()
        redditParser = Parser.Parser("http://www.reddit.com/.json")
        redditStorage = Storage.RedditStorage("reddit.db")

        display = Display.Display()
        tw1 = Display.TextWindow(25, 1600)
        tmw1 = Display.TextMenuWindow(1000, 1600)

        display.registerWindow(tw1)
        display.registerWindow(tmw1)
        pygameEventDispatcher.register(pygame.K_UP, tmw1.moveUp)
        pygameEventDispatcher.register(pygame.K_DOWN, tmw1.moveDown)
        pygameEventDispatcher.register(pygame.K_RETURN, tmw1.select)

        run = True
        lastRedditUpdate = 0
        lastWindowUpdate = 0
        data = None
        while run:
            #get reddit content
            if time.time() - lastRedditUpdate > self.rescrapeTime:
                self.logger.debug("getting reddit content")
                data = redditParser.getContent()
                #store entries
                self.logger.debug("saving content")
                redditStorage.store(data)
                #store update time
                lastRedditUpdate = data.keys()[0]

            #display entries
            if time.time() - lastWindowUpdate > self.windowRefreshTime:
                lastWindowUpdate = time.time()

                #status window
                self.logger.debug("updating status window")
                tw1.deleteLines()
                tw1.addLine("last update: %s" % time.strftime("%c", time.localtime(lastRedditUpdate)))

                self.logger.debug("rendering content")
                tmw1.deleteLines()
                for n in data[lastRedditUpdate]:
                    tmw1.registerEntry("%s by %s" % (n["data"]["title"], n["data"]["author"]), dummy)

                self.logger.debug("display content")
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
