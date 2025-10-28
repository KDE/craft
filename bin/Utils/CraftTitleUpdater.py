import threading
import time

import shells
from CraftCore import CraftCore
from Package.VirtualPackageBase import VirtualPackageBase


class CraftTitleUpdater(object):
    def __init__(self):
        self.doUpdateTitle = True
        self.title = None
        self.timer = None
        self.dynamicMessage = None
        self.dynamicStopMessage = None
        self.progress = None

    def __str__(self):
        dynamicPart = ""
        if self.dynamicMessage:
            dynamicPart = f"{CraftTitleUpdater.br()}{self.dynamicMessage()}"
        return f"{self.title}{CraftTitleUpdater.br()}Duration: {self.timer}{dynamicPart}"

    def updateTitle(self):
        shells.setConsoleTitle(str(self))
        if CraftTitleUpdater.instance.progress:
            shells.setConsoleProgress(CraftTitleUpdater.instance.progress())

    @staticmethod
    def br():
        return "\n\t" if CraftCore.settings.ciMode else " "

    def run(self):
        while self.doUpdateTitle:
            self.updateTitle()
            time.sleep(10)

    def start(self, message, timer):
        self.title = message
        self.timer = timer
        if CraftCore.settings.ciMode:
            return
        self.doUpdateTitle = True
        tittleThread = threading.Thread(target=self.run, daemon=True)
        tittleThread.start()

    def stop(self):
        if self.dynamicStopMessage:
            CraftCore.log.info(self.dynamicStopMessage())
        self.doUpdateTitle = False

    @staticmethod
    def usePackageProgressTitle(packages):
        initialSize = len(packages)

        # the code here works as lists are passed by reference
        def progress():
            print(len(packages), initialSize)
            return int((1 - len(packages) / initialSize) * 100)

        def title():
            if not packages:
                CraftTitleUpdater.instance.dynamicMessage = None
                return ""

            return f"Progress: {progress()}%{CraftTitleUpdater.br()}Remaining Packages: {[x.path for x in packages if not isinstance(x.instance, VirtualPackageBase)]}"

        def stopMessage():
            if not packages:
                return ""
            return f"Craft stopped with out completing {[x.path for x in packages]}"

        CraftTitleUpdater.instance.dynamicMessage = title
        CraftTitleUpdater.instance.dynamicStopMessage = stopMessage
        CraftTitleUpdater.instance.progress = progress
