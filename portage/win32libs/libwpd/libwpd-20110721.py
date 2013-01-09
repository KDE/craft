import os
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.9.0'] = "http://download.sourceforge.net/libwpd/libwpd-0.9.0.tar.bz2"
        self.targetInstSrc['0.9.0'] = "libwpd-0.9.0"
        self.targetDigests['0.9.0'] = 'd667654a329509c458f6e425868fa56ac12cd6b8'
        self.patchToApply['0.9.0'] = ( 'libwpd-0.9.0-20110721.diff', 1 )

        self.shortDescription = "A library designed to help process WordPerfect documents"
        self.defaultTarget = '0.9.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
