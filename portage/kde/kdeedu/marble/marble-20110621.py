import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:marble'
        self.patchToApply[ 'gitHEAD' ] = [ ( "0001-added-first-version-of-flightgear-position-provider-.patch_", 1 ) ]
        self.shortDescription = 'the desktop globe'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.buildDependencies['win32libs-sources/nmealib-src'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
