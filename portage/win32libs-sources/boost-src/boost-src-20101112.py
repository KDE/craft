import os
import shutil

import utils
import base
import info
import compiler

class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['1.44.0'] = 'http://downloads.sourceforge.net/boost/boost_1_44_0.tar.bz2'
        self.targetDigests['1.44.0'] = '0dfeaad7a316ddfdcdb8a7e42443ef048ad18c01'
        self.targetInstSrc['1.44.0'] = 'boost_1_44_0'
        self.defaultTarget = '1.44.0'
        self.shortDescription = "portable C++ libraries"

    def setDependencies(self):
        self.buildDependencies['dev-util/bjam'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.defines = (
                " --build-type=minimal"
                " --build-dir=" + self.buildDir() + \
                " --prefix=" + self.imageDir() + \
                " --stagedir=" + os.path.join(self.buildDir(),"stage") + \
                " threading=multi"
                " link=shared"
                " runtime-link=shared")

        self.subinfo.options.configure.defines += " variant="
        if self.buildType() == "Debug":
            self.subinfo.options.configure.defines += "debug"
        else:
            self.subinfo.options.configure.defines += "release"
        self.subinfo.options.configure.defines += " toolset="
        if compiler.isMinGW():
            self.subinfo.options.configure.defines += "gcc"
        else:
            self.subinfo.options.configure.defines += "msvc"
        if self.isHostBuild():
            self.subinfo.options.configure.defines += " --with-program_options"
        if not emergePlatform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines += " --with-python"

    def configure(self):
        return True

    def install(self):
        self.enterSourceDir()
        cmd  = "bjam install"
        cmd += self.subinfo.options.configure.defines
        if utils.verbose() >= 1:
            print cmd
        os.system(cmd) and utils.die(
                "command: %s failed" % (cmd))
        shutil.copytree(os.path.join(self.imageDir(), "lib"),
                         os.path.join(self.imageDir(), "bin"),
                         ignore=shutil.ignore_patterns('*.a','*.lib'))
        shutil.move(os.path.join(self.imageDir(), "include", "boost-1_44",
                    "boost"),
                    os.path.join(self.imageDir(),"include","boost"))
        shutil.rmtree(os.path.join(self.imageDir(),"include","boost-1_44"))
        if self.isTargetBuild():
            shutil.rmtree(os.path.join(self.imageDir(), "lib"))
            shutil.rmtree(os.path.join(self.imageDir(), "bin"))
        return True

    def runTest(self):
        return False

    def make(self):
        self.enterSourceDir()
        cmd  = "bjam stage"
        cmd += self.subinfo.options.configure.defines
        if utils.verbose() >= 1:
            print cmd
        os.system(cmd) and utils.die(
                "command: %s failed" % (cmd))
        return True

if __name__ == '__main__':
    Package().execute()
