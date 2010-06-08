import info


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "20100605"
        self.targets[ ver ] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/MSYS-"+ver+".zip"
        self.targetDigests[ ver ] = '442c1a44f5ec791c8b9ffd8ff19c09e6fae01af7'
        self.defaultTarget = ver
        
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
