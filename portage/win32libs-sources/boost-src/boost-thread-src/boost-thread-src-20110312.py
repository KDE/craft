import os
import shutil

import utils
import base
import info
import compiler

class subinfo(info.infoclass):
    def setTargets(self):
        self.boost = portage.getPackageInstance('win32libs-sources', 'boost-src')
        self.targets['1.44.0'] = ''
        self.targetInstSrc['1.44.0'] = os.path.join(self.boost.sourceDir(),"libs","thread","build")
        
        self.defaultTarget = '1.44.0'
        self.shortDescription = "portable C++ libraries"

    def setDependencies(self):
        self.buildDependencies['dev-util/bjam'] = 'default'
        self.buildDependencies['win32libs-sources/boost-src'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.boost = portage.getPackageInstance('win32libs-sources', 'boost-src')

        self.subinfo.options.configure.defines = (
                " --build-type=minimal"
                " --build-dir=" + self.buildDir() + \
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
            if compiler.isMSVC2005():
                self.subinfo.options.configure.defines += "msvc-8.0"
            elif compiler.isMSVC2008():
                self.subinfo.options.configure.defines += "msvc-9.0"
            elif compiler.isMSVC2010():
                self.subinfo.options.configure.defines += "msvc-10.0"
                
    def configure(self):
        return True

    def walk(self, directory):
        for f in os.listdir(directory):
          path = os.path.join(directory,f)
          if os.path.isdir(path):
              return self.walk(path)
          if f.endswith("dll"):
              return directory,f
      
    def install(self):
        path,dll = self.walk(self.buildDir())
        utils.copyFile(os.path.join(path,dll),os.path.join(self.imageDir(),"lib",dll))
        utils.copyFile(os.path.join(path,dll),os.path.join(self.imageDir(),"bin",dll))
        if compiler.isMinGW():
            lib = dll + ".a"
        elif compiler.isMSVC():
          lib = dll[0:-3] + "lib"
        utils.copyFile(os.path.join(path,lib),os.path.join(self.imageDir(),"lib",lib))
        return True

    def runTest(self):
        return False

    def make(self):
        self.enterSourceDir()
        cmd  = "bjam"
        cmd += self.subinfo.options.configure.defines
        if utils.verbose() >= 1:
            print cmd
        os.system(cmd) and utils.die(
                "command: %s failed" % (cmd))
        return True

if __name__ == '__main__':
    Package().execute()
