import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:marble'
        self.patchToApply[ 'gitHEAD' ] = [("0001-first-version-of-flightgear-position-provider-plugin.patch_", 1),
                                          ("0003-compile-fix.patch_", 1),
                                          ("0004-listen-on-any-address-to-support-mapping-over-networ.patch_", 1),
                                         ]
        self.shortDescription = 'the desktop globe'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        # TODO: how to limit to gitHEAD for now
        self.buildDependencies['win32libs-sources/nmealib-src'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
