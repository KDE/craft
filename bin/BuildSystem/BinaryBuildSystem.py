#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# installing binary packages

from BuildSystem.BuildSystemBase import *


class BinaryBuildSystem(BuildSystemBase):
    def __init__(self):
        BuildSystemBase.__init__(self, "binary")

    def configure(self):
        return True

    def make(self):
        return True

    def install(self):
        if not BuildSystemBase.install(self):
          return False
        return utils.copyDir(self.sourceDir(), self.installDir(), linkOnly=False)

    def runTest(self):
        return False
