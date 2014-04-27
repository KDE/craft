import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['1.2.16'] = 'http://oligarchy.co.uk/xapian/1.2.16/xapian-core-1.2.16.tar.xz'
        self.targetInstSrc['1.2.16'] = 'xapian-core-1.2.16'
        self.patchToApply['1.2.16'] = [('xapian-core-1.2.16-20131221.diff', 1)]
        self.defaultTarget = '1.2.16'

    def setDependencies( self ):
        self.dependencies['win32libs/zlib'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)

