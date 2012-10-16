import logging
import Parser
import Storage
import time

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG, filename="main.log")
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("main")

    redditParser = Parser.Parser("http://www.reddit.com/.json")
    redditStorage = Storage.RedditStorage("reddit.db")

    sleepTime = 30

    while True:
        #get reddit content
        data = redditParser.getContent()
        #store entries
        redditStorage.store(data)
        #display entries
        #render content
        #save displayed entries


        logger.debug("sleeping for %i seconds" % sleepTime)
        time.sleep(sleepTime)
