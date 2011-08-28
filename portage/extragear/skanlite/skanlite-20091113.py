# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:skanlite.git'
        self.shortDescription = 'a simple scanning application'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['virtual/kdegraphics'] = 'default'

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
