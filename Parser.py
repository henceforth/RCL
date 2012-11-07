#! /bin/python

import time
import os
import urllib2
import json
import logging
import pydoc
#logging.basicConfig(level=logging.DEBUG, filename="logs/Parser.log")

class Parser(object):
    '''parser that allows getting of urls and parsing them from json to actual objects
    '''
    saveFile = "save.json"
    logger =None
    forceRefresh = True

    def __init__(self, url):
        self.url = url
        self.logger = logging.getLogger(self.url)
        self.logger.setLevel(logging.INFO)
        self.logger.info("parser url: %s" % self.url)

    def getContent(self):
        '''scrapes the url and returns the resolved json objects'''
        if not os.path.exists(self.saveFile) or self.forceRefresh:
            if self.forceRefresh:
                self.logger.info("forced refreshing")

            self.logger.info("scraping %s" % self.url)
            request = urllib2.Request(self.url)
            request.add_header("User-agent", "have no fear, rscrape by /u/hcf is here")
            response = urllib2.urlopen(request)
            jsonData = response.read()

            self.logger.debug( response.info())

            tmpFile = open(self.saveFile, "w")
            tmpFile.write(jsonData)
            tmpFile.close()
        else:
            self.logger.info( "loading json from disk")
            jsonData = open(self.saveFile, "r").read()


        self.logger.info( "got %i bytes" % len(jsonData))
        jsonObj = json.loads(jsonData)
        entries = jsonObj["data"]["children"]

        i = 0

        #for n in entries:
            #i+=1
            #self.logger.debug( "%i: %s by %s at %s" % (i, n["data"]["title"], n["data"]["author"], n["data"]["created_utc"]))
                
        self.logger.debug("got %i objects" % len(jsonObj["data"]["children"]))

        #return entries packed with a time stamp
        return {time.time() : entries}

