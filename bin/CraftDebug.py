import functools
import inspect
import logging
import logging.handlers
import os
import re
import shutil
import sys

from CraftConfig import craftSettings
from CraftStandardDirs import CraftStandardDirs


class CraftDebug(object):
    __instance = None

    @staticmethod
    def instance():
        if not CraftDebug.__instance:
            CraftDebug.__instance = CraftDebug()
        return CraftDebug.__instance

    def __init__(self):
        self.seenDeprecatedFunctions = set()
        self._handler = logging.StreamHandler(sys.stdout)

        self._log = logging.getLogger("craft")
        self._log.setLevel(logging.DEBUG)
        self._log.addHandler(self._handler)
        self._handler.setLevel(logging.INFO)

        logDir = craftSettings.get("CraftDebug", "LogDir", os.path.expanduser("~/.craft/"))
        if not os.path.exists(logDir):
            os.makedirs(logDir)

        cleanNameRe = re.compile(r":?\\+|/+|:|;")
        logfileName = os.path.join(logDir, "log-%s.txt" % cleanNameRe.sub("_", CraftStandardDirs._deSubstPath(
            CraftStandardDirs.craftRoot())))

        try:
            fileHandler = logging.handlers.RotatingFileHandler(logfileName, mode="at+", maxBytes=10000000,
                                                               backupCount=20)
            fileHandler.doRollover()
            fileHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
            self._log.addHandler(fileHandler)
            fileHandler.setLevel(logging.DEBUG)
        except Exception as e:
            print(f"Failed to setup log file: {e}", file=sys.stderr)
            print(f"Right now we don't support running multiple Craft instances with the same configuration.",
                  file=sys.stderr)
        self.log.debug("#" * self.lineWidth)
        self.log.debug("New log started: %s" % " ".join(sys.argv))
        self.log.debug("Log is saved to: %s" % fileHandler.baseFilename)
        self.logEnv()
        self.setVerbose(0)

    @property
    def lineWidth(self):
        width, _ = shutil.get_terminal_size((80, 20))
        return width

    def verbose(self):
        """return the value of the verbose level"""
        return self._verbosity

    def setVerbose(self, _verbose):
        self._verbosity = _verbose
        lvl = logging.INFO
        if 0 <= _verbose < 2:
            lvl = logging.INFO
        elif _verbose >= 2:
            lvl = logging.DEBUG
        elif _verbose == 0:
            lvl = logging.WARNING
        elif _verbose <= -1:
            lvl = logging.CRITICAL
        self._handler.setLevel(lvl)

    def step(self, message):
        self.log.info("*** %s ***" % message)

    def new_line(self):
        self.log.info("\n")

    def debug_line(self):
        self.log.info("=" * self.lineWidth)

    @property
    def log(self):
        return self._log

    def print(self, msg):
        if self.verbose() >= 0:
            print(msg)

    def logEnv(self, env=None):
        if craftSettings.getboolean("CraftDebug", "LogEnvironment", True):
            if not env:
                env = os.environ
            self.log.debug(
                "Environment: \n" + "\n".join(f"    {key}={value}" for key, value in env.items()))

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
        msg = f"{fun.__name__} is deprecated"
        if replacement is not None:
            msg += f"; use {replacement} instead"
        if fun.__doc__ is None:
            fun.__doc__ = msg

        @functools.wraps(fun)
        def inner(*args, **kwargs):
            _info = inspect.stack()[1]
            if not (_info.filename, _info.lineno) in craftDebug.seenDeprecatedFunctions:
                craftDebug.seenDeprecatedFunctions.add((_info.filename, _info.lineno))
                if craftDebug.verbose() < 1 and craftDebug.getboolean("CraftDebug", "LogDeprecated", False):
                    craftDebug.print(msg)
                craftDebug.log.debug(msg, stack_info=True)
            return fun(*args, **kwargs)

        return inner

    return outer


if __name__ == "__main__":
    craftDebug.log.debug("debug: foo")
    craftDebug.log.info("info: foo")
