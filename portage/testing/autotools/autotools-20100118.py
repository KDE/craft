import info
import shutil

class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "20100118"
        self.targets[ ver ] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/autotools-"+ver+".tar.bz2"
        self.targetDigests[ ver ] = 'dfb63c7894e1b373df49120988726bc736ac8ba5'
        
        self.defaultTarget = ver
        
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['dev-util/msys'] = 'default'
        self.hardDependencies['testing/libtool-src'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "msys/opt"

if __name__ == '__main__':
    Package().execute()
