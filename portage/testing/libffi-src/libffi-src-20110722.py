# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '3.0.10rc8' ] = "ftp://sources.redhat.com/pub/libffi/libffi-3.0.10rc8.tar.gz"
        self.targetInstSrc[ '3.0.10rc8' ] = "libffi-3.0.10rc8"
        self.targetDigests['3.0.10rc8'] = '1dc449254c4c8bde1f422955e378016ba748d3f2'
        self.patchToApply['3.0.10rc8'] = [("libffi-3.0.10rc8-20110722.diff", 1)]
        self.defaultTarget = '3.0.10rc8'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'


class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()