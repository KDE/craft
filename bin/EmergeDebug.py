import sys

from EmergeConfig import emergeSettings


class Verbose(object):
    """
        This class will work on the overall output verbosity
        It defines the interface for the option parser but before the default
        value is taken from the environment variable.
        There is only one verbosity value for all parts of emerge.
        Always updates the shell variable EMERGE_VERBOSE.
    """
    __level = 0

    @staticmethod
    def increase():
        """increase verbosity"""
        Verbose.setLevel(Verbose.__level + 1)

    @staticmethod
    def decrease():
        """decrease verbosity"""
        Verbose.setLevel(Verbose.__level - 1)

    @staticmethod
    def level():
        return Verbose.__level

    @staticmethod
    def setLevel(newLevel):
        """ set the level by hand for quick and dirty changes """
        Verbose.__level = max(-1, newLevel)

    def verbose( self ):
        """ returns the verbosity level for the application """
        return Verbose.__level


class TemporaryVerbosity(object):
    """Context handler for temporarily different verbosity"""
    def __init__(self, tempLevel):
        self.prevLevel = verbose()
        setVerbose(tempLevel)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trback):
        setVerbose(self.prevLevel)


def verbose():
    """return the value of the verbose level"""
    return Verbose.level()


def setVerbose( _verbose ):
    Verbose.setLevel(_verbose)


def info( message ):
    if verbose() >= 0:
        print("*** %s ***" % message)
    return True


def debug( message, level=1 ):
    if verbose() > level and verbose() > 0:
        print("emerge debug (%s): %s" % (level, message))
        sys.stdout.flush()
    return True


def warning( message ):
    try:
        print("emerge warning: %s" % message)
    except UnicodeEncodeError:
        print("emerge warning: failed to print message")
    return True


def new_line( level=0 ):
    if verbose() > level and verbose() > 0:
        print()


def debug_line( level=0 ):
    if verbose() > level and verbose() > 0:
        print("_" * 80)


def error( message ):
    print("emerge error: %s" % message, file=sys.stderr)
    return False


def die( message ):
    raise Exception("emerge fatal error: %s" % message)


def traceMode():
    """return the value of the trace level"""
    return int(emergeSettings.get( "General", "EMERGE_TRACE", "0" ))


def trace( message, dummyLevel=0 ):
    if traceMode(): #> level:
        print("emerge trace:", message)
    sys.stdout.flush()
    return True