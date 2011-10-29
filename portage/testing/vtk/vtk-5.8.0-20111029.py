import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['5.8.0'] = 'http://www.vtk.org/files/release/5.8/vtk-5.8.0.tar.gz'
        self.targetInstSrc['5.8.0'] = 'VTK'
        self.targetDigests['5.8.0'] = 'ece52f4fa92811fe927581e60ecb39a8a5f68cd9'
        self.defaultTarget = '5.8.0'

    def setDependencies( self ):
        self.shortDescription = "The Visualization Toolkit (VTK) is an open-source, freely available software system for 3D computer graphics, image processing and visualization"
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/jpeg'] = 'defailt'
        self.dependencies['win32libs-bin/libxml2'] = 'defailt'
        self.dependencies['win32libs-bin/tiff'] = 'defailt'
        self.dependencies['win32libs-bin/expat'] = 'defailt'
        self.dependencies['win32libs-bin/zlib'] = 'defailt'
        
from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
