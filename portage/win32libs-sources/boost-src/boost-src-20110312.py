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

from Package.BoostPackageBase import *

class Package(BoostPackageBase):
    def __init__(self, **args):
        self.subinfo = subinfo()
        BoostPackageBase.__init__(self)
        

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
        #disable autolinking
        f = open(os.path.join(self.imageDir(),"include", "boost", "config", "user.hpp"), 'a')
        f.write('#define BOOST_ALL_NO_LIB\n')
        f.close()
        return True


    def make(self):
        self.enterSourceDir()
        cmd  = "bjam stage"
        cmd += self.configureOptions(self.subinfo.options.configure.defines)
        if utils.verbose() >= 1:
            print cmd
        os.system(cmd) and utils.die(
                "command: %s failed" % (cmd))
        return True

if __name__ == '__main__':
    Package().execute()
