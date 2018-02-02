#
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#

"""@package provides simple makefile based build system without any configure step"""

from BuildSystem.BuildSystemBase import *


class MakeFileBuildSystem(BuildSystemBase):
    """ make file build support """

    def __init__(self):
        """constructor. configureOptions are added to the configure command line and makeOptions are added to the make command line"""
        BuildSystemBase.__init__(self, "makefile")

    def configure(self, dummyDefines=""):
        """implements configure step for cmake projects"""

        return True

    def make(self):
        """implements the make step for Makefile projects"""
        if not self.subinfo.options.useShadowBuild:
            self.enterSourceDir()
        else:
            self.enterBuildDir()

        return utils.system([self.makeProgram, self.makeOptions()])

    def install(self):
        """install the target"""
        if not BuildSystemBase.install(self):
            return False

        if not self.subinfo.options.useShadowBuild:
            self.enterSourceDir()
        else:
            self.enterBuildDir()
        return utils.system([self.makeProgram, "install", f"DESTDIR={self.installDir()}"])

    def unittest(self):
        """running make tests"""
        if not self.subinfo.options.useShadowBuild:
            self.enterSourceDir()
        else:
            self.enterBuildDir()

        return utils.system([self.makeProgram, "test"])
