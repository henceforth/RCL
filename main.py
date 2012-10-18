import logging
import Parser
import Storage
import time
import Display
import Dispatcher

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
        tw1 = Display.TextWindow()
        display.registerWindow(tw1)

        run = True
        lastRedditUpdate = 0
        lastWindowUpdate = 0
        data = None
        while run:
            #get reddit content
            if time.time() - lastRedditUpdate > self.rescrapeTime:
                self.logger.info("getting reddit content")
                data = redditParser.getContent()
                #store entries
                self.logger.info("saving content")
                redditStorage.store(data)
                #store update time
                lastRedditUpdate = data.keys()[0]

            #display entries
            if time.time() - lastWindowUpdate > self.windowRefreshTime:
                lastWindowUpdate = time.time()
                tw1.render("last update: %s" % time.strftime("%c", time.localtime(lastRedditUpdate)))
                self.logger.info("rendering content")
                for n in data[lastRedditUpdate]:
                    tw1.render("%s by %s" % (n["data"]["title"], n["data"]["author"]))

                self.logger.info("display content")
                display.update()

            #render selected in contentWindow
            #save displayed entries

            #self.logger.info("dispatching")
            pygameEventDispatcher.check()

            #self.logger.info("sleeping for %f seconds" % self.sleepTime)
            time.sleep(self.sleepTime)

        self.logger.info("shutting down...")


if __name__ == "__main__":
    r1 = Runner()
    r1.run()
