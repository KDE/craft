import EmergeConfig
import EmergeDebug

import datetime

class Timer(object):
    def __init__(self, name, verbosity = 0):
        self.name = name
        self.startTime = None
        self.verbosity = verbosity

    def __enter__(self):
        self.startTime = datetime.datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if EmergeConfig.emergeSettings.getboolean( "EmergeDebug", "MeasureTime", False ):
            EmergeDebug.info( "Task: %s stopped after: %s" % (self.name , datetime.datetime.now() - self.startTime) )
