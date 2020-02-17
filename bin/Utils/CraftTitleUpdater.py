import threading
import time

import utils

from CraftCore import CraftCore

class CraftTitleUpdater(object):
    def __init__(self):
        self.doUpdateTitle = True
        self.title = None
        self.timer = None
        self.dynamicMessage = None
        self.dynamicStopMessage = None

    def __str__(self):
        dynamicPart = ""
        if self.dynamicMessage:
            dynamicPart = f" {self.dynamicMessage()}"
        return f"{self.title}: {self.timer}{dynamicPart}"

    def updateTitle(self):
        utils.OsUtils.setConsoleTitle(str(self))

    def run(self):
        while (self.doUpdateTitle):
            self.updateTitle()
            time.sleep(10)

    def start(self, message, timer):
        self.title = message
        self.timer = timer
        if CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False):
            return
        self.doUpdateTitle = True
        tittleThread = threading.Thread(target=self.run)
        tittleThread.setDaemon(True)
        tittleThread.start()

    def stop(self):
        if self.dynamicStopMessage:
            CraftCore.log.info(self.dynamicStopMessage())
        self.doUpdateTitle = False


    @staticmethod
    def usePackageProgressTitle(packages):
        initialSize = len(packages)
        def title():
            if not packages:
                CraftTitleUpdater.instance.dynamicMessage = None
                return ""
            progress = int((1 - len(packages) / initialSize) * 100)
            return f"{progress}% {[x.path for x in packages]}"

        def stopMessage():
            if not packages:
                return ""
            return f"Craft stopped with out completing {[x.path for x in packages]}"
        CraftTitleUpdater.instance.dynamicMessage = title
        CraftTitleUpdater.instance.dynamicStopMessage = stopMessage
