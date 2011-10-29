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

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        #using our freetipe fails
        self.subinfo.options.configure.defines ="-DBUILD_TESTING=OFF -DVTK_USE_QT=ON -DVTK_USE_SYSTEM_ZLIB=ON -DVTK_USE_SYSTEM_JPEG=ON -DVTK_USE_SYSTEM_PNG=ON -DVTK_USE_SYSTEM_TIFF=ON -DVTK_USE_SYSTEM_EXPAT=ON -DVTK_USE_SYSTEM_LIBXML2=ON "

if __name__ == '__main__':
    Package().execute()
