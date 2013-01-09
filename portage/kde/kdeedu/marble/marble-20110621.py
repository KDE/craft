import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:marble'
        self.patchToApply[ 'gitHEAD' ] = [("0004-listen-on-any-address-to-support-mapping-over-networ.patch_", 1)]
        self.shortDescription = 'the desktop globe'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.buildDependencies['win32libs/nmealib-src'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
