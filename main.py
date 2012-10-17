import logging
import Parser
import Storage
import time
import Display
import pygame#todo: keyboard handler

logging.basicConfig(level=logging.DEBUG, filename="logs/main.log")
logging.captureWarnings(True)

if __name__ == "__main__":
    logger = logging.getLogger("main")

    redditParser = Parser.Parser("http://www.reddit.com/.json")
    redditStorage = Storage.RedditStorage("reddit.db")

    sleepTime = 0.01

    display = Display.Display()
    tw1 = Display.TextWindow()
    display.registerWindow(tw1)

    run = True
    lastUpdate = 0
    while run:
        #update every 30 seconds
        if time.time() - lastUpdate > 30:
            lastUpdate = time.time()
            #get reddit content
            logger.info("getting reddit content")
            data = redditParser.getContent()
            #store entries
            logger.info("saving content")
            redditStorage.store(data)

        #display entries
        logger.info("rendering content")
        tw1.render("text to render")
        #render selected in contentWindow
        #update screen
        logger.info("display content")
        display.update()
        #save displayed entries

        #check keyboard input
        curEvent = pygame.event.poll()
        while curEvent.type != pygame.NOEVENT:
            print curEvent
            if curEvent.type == pygame.KEYDOWN:
                if curEvent.key == pygame.K_q:
                    run = False
                    break
            curEvent = pygame.event.poll()

        logger.info("sleeping for %i seconds" % sleepTime)
        time.sleep(sleepTime)

    logger.info("shutting down...")

