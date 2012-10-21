import logging

class FunctionCallObject(object):
    '''
    object that provides an easy interface for function hooks
    registers a function and its arguments on creation
    and calls them when itself is called
    '''
    function = None
    argList = None
    logger = None

    def __init__(self, functionToCall, *args):
        self.logger = logging.getLogger("funcCallObj")
        self.function = functionToCall
        self.argList = []
        if len(args)>0:
            for n in args:
                self.argList.append(n)

        self.logger.debug("created entry for %s, %i arguments" % (functionToCall, len(args)))

    def __call__(self, *args):
        '''the args provided for this function will not be used here
        instead this class must be derived to support new functionality
        '''
        #ignore args
        self.logger.debug("calling %s" % self.function)
        if len(self.argList) > 0:
            self.function(*self.argList)
        else:
            self.function()
