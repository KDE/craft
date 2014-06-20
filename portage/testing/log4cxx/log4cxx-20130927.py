# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['0.10.0'] = 'http://apache.osuosl.org/logging/log4cxx/0.10.0/apache-log4cxx-0.10.0.tar.gz'
        self.targetInstSrc['0.10.0'] = 'apache-log4cxx-0.10.0'
        self.patchToApply['0.10.0'] = [
                                        ('apache-log4cxx-0.10.0-20130927.diff', 1),
                                        ('apache-log4cxx-0.10.0-cmake.diff', 1)
                                      ]
        self.defaultTarget = '0.10.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['testing/apr-src'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()