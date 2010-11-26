import info
import shutil

class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "20100923"
        self.targets[ ver ] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/autotools-"+ver+".tar.xz"
        self.targetDigests[ ver ] = '73fe57bec9f3813556a38602daf4e9ea9b4b0dba'
        
        self.defaultTarget = ver
        
    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'
        self.buildDependencies['dev-util/7zip'] = 'default'
        self.dependencies['dev-util/msys'] = 'default'
        self.dependencies['testing/libtool-src'] = 'default'
        
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
