import info


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "20100911"
        self.targets[ ver ] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/MSYS-"+ver+".zip"
        self.targetDigests[ ver ] = '5418e36841c0ef11e4f455a31d0580fbc2599917'
        self.defaultTarget = ver
        
    
    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'
        
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
