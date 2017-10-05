import ctypes
import os
import subprocess

import CraftConfig
import CraftDebug
import CraftStandardDirs
from CraftOS.osutils import OsUtils
from Notifier.NotificationInterface import *

class Snore(NotificationInterface):
    def __init__(self):
        NotificationInterface.__init__(self, "Snore")
        self.icon = os.path.join(CraftStandardDirs.CraftStandardDirs.craftBin(), "data", "icons", "craftyBENDER.png")

    def notify(self, title, message, alertClass):
        try:
            snore = CraftCore.cache.findApplication("snoresend")
            if not snore:
                return
            command = f"""{snore} -t "{title}" -m "{message}" -i "{self.icon}" -a "Craft" -c "{alertClass}" --silent """
            if OsUtils.isWin():
                command += f" --bring-window-to-front {ctypes.windll.kernel32.GetConsoleWindow()}"
            CraftDebug.CraftCore.log.debug(command)
            subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL,
                             cwd=CraftStandardDirs.CraftStandardDirs.craftRoot())  # make sure that nothing is spawned in a build dir
        except Exception as e:
            CraftDebug.CraftCore.log.debug(e)
            return
