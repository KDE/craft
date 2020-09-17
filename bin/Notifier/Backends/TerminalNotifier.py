import ctypes
import os
import subprocess

from CraftOS.osutils import OsUtils
from Notifier.NotificationInterface import *
from CraftCore import CraftCore
import utils

class TerminalNotifier(NotificationInterface):
    def __init__(self):
        NotificationInterface.__init__(self, "TerminalNotifier")
        self.icon = os.path.join(CraftCore.standardDirs.craftBin(), "data", "icons", "craftyBENDER.png")

    def notify(self, title, message, alertClass):
        try:
            tn = CraftCore.cache.findApplication("terminal-notifier")
            if not tn:
                return
            command = [tn, "-title", title, "-message", message, "-appIcon", self.icon]
            CraftCore.log.debug(command)
            subprocess.Popen(command,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            cwd=CraftCore.standardDirs.craftRoot())  # make sure that nothing is spawned in a build dir
        except Exception as e:
            CraftCore.log.debug(e)
            return
