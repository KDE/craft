import ctypes
import os
import subprocess

import CraftConfig
import CraftDebug
from CraftOS.osutils import OsUtils
from Notifier.NotificationInterface import *
from utils import utilsCache


class Snore(NotificationInterface):
    def __init__(self):
        NotificationInterface.__init__(self, "Snore")
        self.icon = os.path.join(CraftConfig.CraftStandardDirs.craftBin(), "data", "icons", "craftyBENDER.png")

    def notify(self, title, message, alertClass):
        try:
            snore = utilsCache.findApplication("snoresend")
            if not snore:
                return
            command = """%s -t "%s" -m "%s" -i "%s" -a "Craft" -c "%s" --silent """ % (
            snore, title, message, self.icon, alertClass)
            if OsUtils.isWin():
                command += " --bring-window-to-front %s" % ctypes.windll.kernel32.GetConsoleWindow()
            CraftDebug.craftDebug.log.debug(command)
            subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL,
                             cwd=CraftConfig.CraftStandardDirs.craftRoot())  # make sure that nothing is spawned in a build dir
        except Exception as e:
            CraftDebug.craftDebug.log.debug(e)
            return
