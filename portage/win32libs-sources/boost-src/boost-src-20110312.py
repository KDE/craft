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
        shutil.copytree(os.path.join(self.sourceDir(), "boost"),
                         os.path.join(self.imageDir(), "include" , "boost"),
                         ignore=shutil.ignore_patterns('*.a','*.lib'))
        #disable autolinking
        f = open(os.path.join(self.imageDir(),"include", "boost", "config", "user.hpp"), 'a')
        f.write('#define BOOST_ALL_NO_LIB\n')
        f.close()
        return True


    def make(self):
        return True

if __name__ == '__main__':
    Package().execute()
