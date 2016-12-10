import inspect
import os
import re
import sys
import logging
import functools

from CraftConfig import craftSettings, CraftStandardDirs

class CraftDebug(object):
    __instance = None

    @staticmethod
    def instance():
        if not CraftDebug.__instance:
            CraftDebug.__instance = CraftDebug()
        return  CraftDebug.__instance

    def __init__(self):
        self.seenDeprecatedFunctions = set()
        self._handler = logging.StreamHandler(sys.stdout)

        self._log = logging.getLogger("craft")
        self._log.setLevel(logging.DEBUG)
        self._log.addHandler(self._handler)
        self._handler.setLevel(logging.INFO)


        logDir = craftSettings.get("General", "EMERGE_LOG_DIR", os.path.expanduser("~/.craft/"))
        if not os.path.exists(logDir):
            os.makedirs(logDir)

        cleanNameRe = re.compile(r":?\\+|/+|:|;")
        fileHandler = logging.FileHandler(os.path.join(logDir, "log-%s.txt" % cleanNameRe.sub("_", CraftStandardDirs._deSubstPath(CraftStandardDirs.craftRoot()))), mode="wt+")
        self._log.addHandler(fileHandler)
        fileHandler.setLevel(logging.DEBUG)
        self.log.debug("Log is saved to: %s" % fileHandler.baseFilename)

    def verbose(self):
        """return the value of the verbose level"""
        lvl = self._handler.level
        if lvl == logging.INFO:
            return 0
        elif lvl <= logging.DEBUG:
            return 3
        else:
            return -1

    def setVerbose(self, _verbose):
        if 0 < _verbose < 2:
            lvl = logging.INFO
        elif _verbose >= 2:
            lvl = logging.DEBUG
        elif _verbose < 0:
            lvl = logging.WARNING
        self._handler.setLevel(lvl)

    def step(self, message):
        self.log.info("*** %s ***" % message)

    def new_line(self):
        self.log.info("\n")

    def debug_line(self):
        self.log.info("_" * 80)

    @property
    def log(self):
        return self._log

    def trace(self, message):
        self.log.debug("craft trace: %s" % message)


craftDebug = CraftDebug.instance()

class TemporaryVerbosity(object):
    """Context handler for temporarily different verbosity"""
    def __init__(self, tempLevel):
        self.prevLevel = craftDebug.verbose()
        craftDebug.setVerbose(tempLevel)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trback):
        craftDebug.setVerbose(self.prevLevel)

def deprecated(replacement=None):
    """
    http://code.activestate.com/recipes/577819-deprecated-decorator/
    Deprecated decorator.

    Author: Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>
    License: MIT
    A decorator which can be used to mark functions as deprecated.
    replacement is a callable that will be called with the same args
    as the decorated function.

    >>> @deprecated()
    ... def foo(x):
    ...     return x
    ...
    >>> ret = foo(1)
    DeprecationWarning: foo is deprecated
    >>> ret
    1
    >>>
    >>>
    >>> def newfun(x):
    ...     return 0
    ...
    >>> @deprecated(newfun)
    ... def foo(x):
    ...     return x
    ...
    >>> ret = foo(1)
    DeprecationWarning: foo is deprecated; use newfun instead
    >>> ret
    0
    >>>
    """

    def outer(fun):
        msg = "%s is deprecated" % fun.__name__
        if replacement is not None:
            msg += "; use %s instead" % replacement
        if fun.__doc__ is None:
            fun.__doc__ = msg

        @functools.wraps(fun)
        def inner(*args, **kwargs):
            _info = inspect.stack()[1]
            if not (_info.filename, _info.lineno) in craftDebug.seenDeprecatedFunctions:
                craftDebug.seenDeprecatedFunctions.add((_info.filename, _info.lineno))
                craftDebug.log.warning(msg)
                craftDebug.log.info("Used in: %s line: %s" % (_info.filename, _info.lineno))
                craftDebug.log.debug("Trace for the usage of %s" % fun.__name__, stack_info=True)
            return fun(*args, **kwargs)

        return inner
    return outer

if __name__ == "__main__":
    craftDebug.log.debug("debug: foo")
    craftDebug.log.info("info: foo")