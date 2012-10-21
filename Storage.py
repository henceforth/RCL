#!/usr/bin/python
import logging
import shelve
import pydoc
#logging.basicConfig(level=logging.DEBUG, filename="logs/Parser.log")

class Storage(object):
    '''thin, abstract database layer
    logic for setting entries must be implemented in Storage::store()
    logic for getting entries must be implemented in Storage::get()
    '''

    saveFile = None
    database = None
    logger = None

    def __init__(self, saveFile):
        self.saveFile = saveFile
        self.logger = logging.getLogger(saveFile)
        self.logger.setLevel(logging.INFO)
        self.logger.info("storage file: %s" % self.saveFile)
        self.database = shelve.open(self.saveFile, writeback=True)

    def __del__(self):
        self.database.close()

    def sync(self):
        '''wrapper method to sync entries with the database'''
        self.database.sync()

    def store(self, data):
        '''must be overridden by implementation to support storage of data'''
        raise Exception("NOT IMPLEMENTED")

    def get(self, key):
        '''must be overridden by implementation to support getting of data'''
        raise Exception("NOT IMPLEMENTED")


class RedditStorage(Storage):
    '''derivate for storing reddit entries
    '''
    def __init__(self, saveFile):
        super(RedditStorage, self).__init__(saveFile)
        self.logger.debug("RedditStorage runs")

    def store(self, data):
        #only one entry should be aviable
        entryArray = data[data.keys()[0]]

        new = 0
        old = 0
        for n in entryArray:
            if not self.database.has_key(str(n["data"]["id"])):
                self.logger.debug( "ADDING: %s" % (n["data"]["title"]))
                self.database[str(n["data"]["id"])] = n["data"]
                new += 1
            else:
                self.logger.debug( "EXISTS: %s" % (n["data"]["title"]))
                old += 1

        self.logger.info("added %i new entries, %i were old, total %i" % (new, old, len(self.database)))

    def get(self, redditPostId):
        self.logger.debug("getting key %s" % redditPostId)
        if self.database.has_key(str(redditPostId)):
            return self.database[redditPostId]
        else:
            return None
