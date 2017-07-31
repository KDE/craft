import CraftConfig
from CraftDebug import craftDebug

import datetime


class Timer(object):
    def __init__(self, name, verbosity=0):
        self.name = name
        self.__startTime = None
        self.__stopTime = None
        self._verbosity = verbosity

    def __enter__(self):
        self.__startTime = datetime.datetime.now()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        if CraftConfig.craftSettings.getboolean("CraftDebug", "MeasureTime", False):
            craftDebug.step("Task: %s stopped after: %s" % (self.name, self))

    def __str__(self):
        out = str(self.duration)
        return out[:out.rfind(".")]  # remove milli seconds

    @property
    def duration(self):
        return self.__stopTime or datetime.datetime.now() - self.__startTime

    def stop(self):
        if not self.__startTime:
            self.__stopTime = datetime.datetime.now()
