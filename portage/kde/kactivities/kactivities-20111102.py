import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kactivities'
        for version in ['4.4', '4.5', '4.6', '4.7', '4.8', '4.9']:
            self.svnTargets[version] = '[git]kde:kactivities|KDE/%s|' % version
        self.defaultTarget = '4.9'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.shortDescription = "KDE Activity Manager"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
