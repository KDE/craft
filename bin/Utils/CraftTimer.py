import datetime

import CraftConfig
from CraftCore import CraftCore


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
        if CraftConfig.CraftCore.settings.getboolean("CraftDebug", "MeasureTime", False):
            CraftCore.debug.step(f"Task: {self.name} stopped after: {self}")

    def __str__(self):
        minutes, seconds = divmod(self.duration.total_seconds(), 60)
        hours, minutes = divmod(minutes, 60)
        def format(time, string):
            time = int(time)
            s = "s" if time != 1 else ""
            return f"{time} {string}{s}"
        out = []
        if hours:
            out.append(format(hours, "hour"))
        if minutes:
            out.append(format(minutes, "minute"))
        out.append(format(seconds, "second"))
        return " ".join(out)

    @property
    def duration(self):
        return self.__stopTime or datetime.datetime.now() - self.__startTime

    def stop(self):
        if not self.__startTime:
            self.__stopTime = datetime.datetime.now()
