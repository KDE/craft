import os
import platform
import sys

class OsDetection(object):
    @staticmethod
    def isWin():
        return os.name == 'nt'


    @staticmethod
    def isUnix():
        return os.name == 'posix'


    @staticmethod
    def isFreeBSD():
        return OsDetection.isUnix() and platform.system() == 'FreeBSD'


    @staticmethod
    def isMac():
        return OsDetection.isUnix() and platform.system() == 'Darwin'


    @staticmethod
    def isLinux():
        return OsDetection.isUnix() and platform.system() == 'Linux'


    @staticmethod
    def name():
        if OsDetection.isWin(): return "win"
        if OsDetection.isFreeBSD(): return "freebsd"
        if OsDetection.isMac(): return "mac"
        if OsDetection.isLinux(): return "linux"
        print("Error:unknown system", file=sys.stderr)
        exit(1)
