import abc
import os
import platform

import sys


class OsUtilsBase(metaclass=abc.ABCMeta):
    @abc.abstractstaticmethod
    def rm(path, force=False):
        """ Removes a file"""
        pass

    @abc.abstractstaticmethod
    def rmDir(path, force=False):
        """ Removes a file"""
        pass

    @abc.abstractstaticmethod
    def getFileAttributes(path):
        """ Returns the attributes"""
        pass

    @abc.abstractstaticmethod
    def removeReadOnlyAttribute(path):
        """ Removes the readonly flag"""
        pass

    def setConsoleTitle(title):
        """ Set the console title """
        return True

    @staticmethod
    def isWin():
        return os.name == 'nt'

    @staticmethod
    def isUnix():
        return os.name == 'posix'

    @staticmethod
    def isFreeBSD():
        return OsUtilsBase.isUnix() and platform.system() == 'FreeBSD'

    @staticmethod
    def isMac():
        return OsUtilsBase.isUnix() and platform.system() == 'Darwin'

    @staticmethod
    def isLinux():
        return OsUtilsBase.isUnix() and platform.system() == 'Linux'

    @staticmethod
    def name():
        if OsUtilsBase.isWin(): return "win"
        if OsUtilsBase.isFreeBSD(): return "freebsd"
        if OsUtilsBase.isMac(): return "mac"
        if OsUtilsBase.isLinux(): return "linux"
        print("Error:unknown system", file=sys.stderr)
        exit(1)

    @staticmethod
    def supportsSymlinks() -> bool:
        return True
