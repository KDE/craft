import threading
import time

import shells
from CraftCore import CraftCore
from Package.VirtualPackageBase import VirtualPackageBase

try:
    from rich.markup import escape
    from rich.text import Text
except ImportError:
    pass


class CraftTitleUpdater(object):
    SPINNER_WIDTH = 2

    def __init__(self):
        self.doUpdateTitle = True
        self.title = None
        self.timer = None
        self.dynamicMessage = None
        self.dynamicStopMessage = None
        self.progress = None
        self.packageStatus = None
        self.console = None
        self.status = None

    def __str__(self):
        dynamicPart = ""
        if self.dynamicMessage:
            dynamicPart = f"{CraftTitleUpdater.br()}{self.dynamicMessage()}"
        return f"{self.title}{CraftTitleUpdater.br()}Duration: {self.timer}{dynamicPart}"

    def statusText(self):
        parts = [f"[bold]{escape(self.title)}[/]", f"[dim]{self.timer}[/]"]
        if self.packageStatus:
            parts.append(self.packageStatus())
        text = Text.from_markup(" · ".join(filter(None, parts)))
        text.truncate(self.console.width - CraftTitleUpdater.SPINNER_WIDTH, overflow="ellipsis")
        return text

    def updateTitle(self):
        shells.setConsoleTitle(str(self))
        if CraftTitleUpdater.instance.progress:
            shells.setConsoleProgress(CraftTitleUpdater.instance.progress())

    @staticmethod
    def br():
        return "\n\t" if CraftCore.settings.ciMode else " "

    def run(self):
        ticks = 0
        while self.doUpdateTitle:
            if self.status:
                self.status.update(self.statusText())
            if ticks % 10 == 0:
                self.updateTitle()
            ticks += 1
            time.sleep(1)

    def start(self, message, timer):
        self.title = message
        self.timer = timer
        if CraftCore.settings.ciMode:
            return
        self.doUpdateTitle = True
        if CraftCore.debug.console and CraftCore.debug.console.is_terminal:
            self.console = CraftCore.debug.console
            self.status = self.console.status(self.statusText())
            self.status.start()
        tittleThread = threading.Thread(target=self.run, daemon=True)
        tittleThread.start()

    def stop(self):
        if self.dynamicStopMessage:
            CraftCore.log.info(self.dynamicStopMessage())
        self.doUpdateTitle = False
        if self.status:
            self.status.stop()
            self.status = None

    @staticmethod
    def usePackageProgressTitle(packages):
        initialSize = len(packages)

        # the code here works as lists are passed by reference
        def progress():
            return int((1 - len(packages) / initialSize) * 100)

        def remaining():
            return [x.path for x in packages if not isinstance(x.instance, VirtualPackageBase)]

        def title():
            if not packages:
                CraftTitleUpdater.instance.dynamicMessage = None
                return ""

            return f"Progress: {progress()}%{CraftTitleUpdater.br()}Remaining Packages: {remaining()}"

        def packageStatus():
            names = remaining()
            if not names:
                return ""
            current, upcoming = names[0], names[1:]
            text = f"[cyan]{escape(current)}[/] {initialSize - len(packages) + 1}/{initialSize} ({progress()}%)"
            if upcoming:
                more = f", +{len(upcoming) - 3} more" if len(upcoming) > 3 else ""
                text += f" [dim]next: {escape(', '.join(upcoming[:3]))}{more}[/]"
            return text

        def stopMessage():
            names = remaining()
            if not names:
                return ""
            return f"Craft stopped without completing {len(names)} package{'s' if len(names) > 1 else ''}: {', '.join(names)}"

        CraftTitleUpdater.instance.dynamicMessage = title
        CraftTitleUpdater.instance.dynamicStopMessage = stopMessage
        CraftTitleUpdater.instance.progress = progress
        CraftTitleUpdater.instance.packageStatus = packageStatus
