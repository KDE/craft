import shutil

from BuildSystem.BuildSystemBase import *


class PipBuildSystem(BuildSystemBase):
    def __init__(self):
        BuildSystemBase.__init__(self, "pip")
        self.python2 = True
        self.python3 = True

    def configure(self):
        return True

    def make(self):
        return True

    def install(self):
        ok = True

        pythons = []
        if self.python2:
            pythons.append("python2")
        if self.python3:
            pythons.append("python3")

        for python in pythons:
            command = [python, "-m", "pip", "install", "--upgrade", self.package.name]
            ok = ok and utils.system(command)
        return ok

    def runTest(self):
        return False
