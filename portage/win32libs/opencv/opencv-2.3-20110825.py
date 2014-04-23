import info
from Package.CMakePackageBase import *
import compiler


if compiler.isMinGW() and os.getenv("EMERGE_USE_CCACHE") == "True":
    os.putenv("CXX","g++")
    os.putenv("CC","gcc")

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.defaultTarget = '2.4.5'
        self.shortDescription = 'a library for real time computer vision'
        
        self.svnTargets['gitHEAD'] = 'git://code.opencv.org/opencv.git'
        
        self.svnTargets['2.3'] = 'http://downloads.sourceforge.net/opencvlibrary/OpenCV-2.3.0-win-src.zip'
        self.targetInstSrc['2.3'] = 'OpenCV-2.3.0'
        
        # 2.4.5 is the first with .tar.gz, previous were .tar.bz2
        for ver in [ '2.4.5' ]:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/opencvlibrary/opencv-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'opencv-' + ver
        
        self.targetDigests['2.3'] = '126787da5a3d71e80eb6e8d3bed126391e0549c9'
        self.targetDigests['2.4.5'] = '9e25f821db9e25aa454a31976ba6b5a3a50b6fa4'
        
        self.patchToApply['2.3'] = ('OpenCV-2.3.0-20110817.diff', 1)
        
        self.options.configure.defines = "-DBUILD_NEW_PYTHON_SUPPORT=OFF"
        

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.make.supportsMultijob = False

if __name__ == '__main__':
    Package().execute()