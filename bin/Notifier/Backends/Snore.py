import ctypes
import os
import subprocess

import utils
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Notifier.NotificationInterface import *


class Snore(NotificationInterface):
    def __init__(self):
        NotificationInterface.__init__(self, "Snore")
        self.icon = os.path.join(CraftCore.standardDirs.craftBin(), "data", "icons", "craftyBENDER.png")

    def notify(self, title, message, alertClass):
        try:
            snore = CraftCore.cache.findApplication("snoresend")
            if not snore:
                return
            command = [
                snore,
                "-t",
                title,
                "-m",
                message,
                "-i",
                self.icon,
                "-a",
                "Craft",
                "--silent",
            ]
            if alertClass:
                command += ["-c", alertClass]
            if OsUtils.isWin():
                command += [
                    "--bring-window-to-front",
                    str(ctypes.windll.kernel32.GetConsoleWindow()),
                ]
            CraftCore.log.debug(command)
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=CraftCore.standardDirs.craftRoot(),
            )  # make sure that nothing is spawned in a build dir
        except Exception as e:
            CraftCore.log.debug(e)
            return
