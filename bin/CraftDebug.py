import inspect
import os
import sys
import logging
import functools

from CraftConfig import craftSettings

class CraftDebug(object):
    __instance = None

    @staticmethod
    def instance():
        if not CraftDebug.__instance:
            CraftDebug.__instance = CraftDebug()
        return  CraftDebug.__instance

    def __init__(self):
        self.seenDeprecatedFunctions = set()
        self._log = logging.getLogger("craft")
        self._log.setLevel(logging.INFO)
        self._log.addHandler(logging.StreamHandler(sys.stdout))
        logDir = craftSettings.get("General", "EMERGE_LOG_DIR", os.path.expanduser("~/.craft/"))
        if not os.path.exists(logDir):
            os.makedirs(logDir)
        logging.getLogger().addHandler(logging.FileHandler(os.path.join(logDir, "log.txt"), "wt+"))

    def verbose(self):
        """return the value of the verbose level"""
        lvl = self.log.level
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
        self.log.setLevel(lvl)

    def step(self, message):
        self.log.info("*** %s ***" % message)

    def new_line(self):
        self.log.info("\n")

    def debug_line(self):
        self.log.info("_" * 80)

    @property
    def log(self):
        return self._log

    def traceMode(self):
        """return the value of the trace level"""
        return int(craftSettings.get("General", "EMERGE_TRACE", "0"))

    def trace(self, message, dummyLevel=0):
        if self.traceMode():  # > level:
            self.log.debug("craft trace: %s" % message)
        return True


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
            return fun(*args, **kwargs)

        return inner
    return outer
