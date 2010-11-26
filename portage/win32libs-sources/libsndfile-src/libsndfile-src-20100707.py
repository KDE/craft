import info

from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['1.0.21'] = 'http://www.mega-nerd.com/libsndfile/files/libsndfile-1.0.21.tar.gz'
        self.targetInstSrc['1.0.21'] = 'libsndfile-1.0.21'
        self.patchToApply['1.0.21'] = ( 'libsndfile-1.0.21-20100708.diff', 1 )
        self.defaultTarget = '1.0.21'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/libogg'] = 'default'
        self.dependencies['win32libs-bin/libvorbis'] = 'default'
        
class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( sel f)

if __name__ == '__main__':
    Package().execute()
