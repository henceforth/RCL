import logging
import Parser
import Storage
import time
import Display

import pygame#todo: keyboard handler

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG, filename="main.log")
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("main")

    redditParser = Parser.Parser("http://www.reddit.com/.json")
    redditStorage = Storage.RedditStorage("reddit.db")

    sleepTime = 30

    display = Display.Display()
    tw1 = Display.TextWindow()
    display.registerWindow(tw1)

    run = True
    while run:
        #get reddit content
        data = redditParser.getContent()
        #store entries
        redditStorage.store(data)
        #display entries
        tw1.render("text to render")
        #render selected in contentWindow
        #update screen
        display.update()
        #save displayed entries

        #check keyboard input
        curEvent = pygame.event.poll()
        if curEvent == pygame.KEYDOWN:
            if curEvent.key == K_q:
                run =False
                break

        logger.debug("sleeping for %i seconds" % sleepTime)
        time.sleep(sleepTime)

    self.logger.debug("shutting down...")

