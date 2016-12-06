import CraftOS.OsUtilsBase
from CraftDebug import craftDebug
import shutil
import os
import sys

class OsUtils(CraftOS.OsUtilsBase.OsUtilsBase):

    @staticmethod
    def rm(path, force=False):
        craftDebug.log.debug("deleting file %s" % path)
        try:
            os.remove(path)
            return True
        except OSError as e:
            craftDebug.log.warning("could not delete file %s: %s" % (path, e))
            return False

    @staticmethod
    def rmDir(path, force=False):
        craftDebug.log.debug("deleting directory %s" % path)
        try:
            shutil.rmtree(path)
            return True
        except OSError:
            return OsUtils.rm(path, force)
        return False

    @staticmethod
    def isLink(path):
        return os.path.islink(path)

    @staticmethod
    def removeReadOnlyAttribute(path):
        return False

    @staticmethod
    def setConsoleTitle(title):
         # TODO: http://www.faqs.org/docs/Linux-mini/Xterm-Title.html
        #sys.stdout.write( "\033]2;%s\007" % title)
        #sys.stdout.flush()
        return True