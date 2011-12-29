import os
import shutil

import utils
import base
import info
import compiler

class subinfo(info.infoclass):
    def setTargets(self):      
        for ver in ['1.44.0','1.47.0','1.48.0']:
              verString = ver.replace('.','_')
              self.targets[ver] = 'http://downloads.sourceforge.net/boost/boost_%s.7z' % verString
              self.targetInstSrc[ver] = 'boost_%s' % verString
        self.patchToApply['1.47.0'] = ('boost_1_47_0-20110815.diff',1)
        self.patchToApply['1.48.0'] = ('boost_1_47_0-20110815.diff',1)
        self.targetDigests['1.48.0'] = 'f221f067620e5af137e415869bd96ad667db9830'

        self.defaultTarget = '1.48.0'
        self.shortDescription = "portable C++ libraries"

    def setDependencies(self):
        self.buildDependencies['virtual/base'] = 'default'
        
from Package.BoostPackageBase import *

class Package(BoostPackageBase):
    def __init__(self, **args):
        self.subinfo = subinfo()
        BoostPackageBase.__init__(self)

    def make(self):
        return True
    
    def install(self):
        shutil.copytree(os.path.join(self.sourceDir(), "boost"),
                        os.path.join(self.imageDir(), "include" , "boost"))        #disable autolinking
        f = open(os.path.join(self.imageDir(),"include", "boost", "config", "user.hpp"), 'a')
        f.write('#define BOOST_ALL_NO_LIB\n')
        f.close()
        return True


if __name__ == '__main__':
    Package().execute()
