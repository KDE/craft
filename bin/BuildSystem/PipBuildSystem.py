import shutil

from BuildSystem.BuildSystemBase import *


class PipBuildSystem(BuildSystemBase):
    def __init__(self):
        BuildSystemBase.__init__(self, "pip")
        self.python2 = True
        self.python3 = True

    @property
    def __pythons(self):
        pythons = []
        if self.python2:
            pythons.append("python2")
        if self.python3:
            pythons.append("python3")
        return pythons

    def configure(self):
        return True

    def make(self):
        if self.subinfo.svnTarget():
            for python in self.__pythons:
                if not utils.system([python, "setup.py", "sdist"], cwd=self.sourceDir()):
                    return True
        return True

    def install(self):
        ok = True

        for python in self.__pythons:
            command = [python, "-m", "pip", "install", "--upgrade"]
            if self.subinfo.svnTarget():
                command += ["-e", self.sourceDir()]
            else:
                command += [self.package.name]
            ok = ok and utils.system(command)
        return ok

    def runTest(self):
        return False
