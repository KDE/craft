#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# installing binary packages

import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from BuildSystem.BuildSystemBase import BuildSystemBase


class BinaryBuildSystem(BuildSystemBase):
    def __init__(self, package: CraftPackageObject):
        BuildSystemBase.__init__(self, package, "binary")

    def configure(self):
        return True

    def make(self):
        return True

    def install(self):
        if not BuildSystemBase.install(self):
            return False
        return utils.copyDir(self.sourceDir(), self.installDir(), linkOnly=False)

    def internalPostInstall(self):
        return True

    def runTest(self):
        return False
