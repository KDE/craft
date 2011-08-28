# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/utils/krecipes'
        self.targets['2.0-alpha3'] = 'http://downloads.sourceforge.net/krecipes/krecipes-2.0-alpha3.tar.gz'
        self.targets['2.0-beta2'] = 'http://downloads.sourceforge.net/krecipes/krecipes-2.0-beta2.tar.gz'
        self.targetDigests['2.0-beta2'] = 'fc232c9125e555d8c1cbbbf5020311ed6f278b39'
        self.targetInstSrc['2.0-alpha3'] = 'krecipes-2.0-alpha3'
        self.targetInstSrc['2.0-beta2'] = 'krecipes-2.0-beta2'
        self.shortDescription = 'a recipes database'
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['virtual/kde-runtime'] = 'default'

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
