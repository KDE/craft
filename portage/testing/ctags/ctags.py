import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['5.8'] = 'http://downloads.sourceforge.net/ctags/ctags-5.8.tar.gz'
        self.patchToApply['5.8'] = [('ctags-5.8-20120828.diff', 1), ('ctags-cmake.diff', 1)]
        self.targetDigests['5.8'] = '482da1ecd182ab39bbdc09f2f02c9fba8cd20030'
        self.targetInstSrc['5.8'] = 'ctags-5.8'
        self.defaultTarget = '5.8'

class Package(CMakePackageBase):
    def __init__( self ):
        # we use subinfo for now too
        CMakePackageBase.__init__( self )


