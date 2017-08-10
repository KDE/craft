import threading
import time

import utils


class CraftTitleUpdater(object):
    def __init__(self):
        self.doUpdateTitle = True
        self.title = None
        self.timer = None
        self.dynamicMessage = None

    def run(self):
        while (self.doUpdateTitle):
            dynamicPart = ""
            if self.dynamicMessage:
                dynamicPart = f" {self.dynamicMessage()}"
            utils.OsUtils.setConsoleTitle(f"{self.title}: {self.timer}{dynamicPart}")
            time.sleep(1)

    def start(self, message, timer):
        self.title = message
        self.timer = timer
        self.doUpdateTitle = True
        tittleThread = threading.Thread(target=self.run)
        tittleThread.setDaemon(True)
        tittleThread.start()

    def stop(self):
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
        CraftTitleUpdater.instance.dynamicMessage = title
