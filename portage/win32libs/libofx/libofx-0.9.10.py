import info
import compiler

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['0.9.10'] = "http://downloads.sourceforge.net/project/libofx/libofx/0.9.10/libofx-0.9.10.tar.gz"
        self.targetDigests['0.9.10'] = '33f394c963c087217cb6c508af842d4844bc0823'
        self.targetInstSrc['0.9.10'] = "libofx-0.9.10"
        self.patchToApply['0.9.10'] = [("libofx-0.9.5-20120131.diff", 1)]

        self.shortDescription = "a parser and an API for the OFX (Open Financial eXchange) specification"
        self.defaultTarget = '0.9.10'

    def setDependencies( self ):
        self.dependencies['win32libs/libopensp'] = 'default'
        self.dependencies['win32libs/win_iconv'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        # we use subinfo for now too
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

