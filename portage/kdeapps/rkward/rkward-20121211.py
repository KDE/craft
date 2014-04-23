import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'svnHEAD' ] = 'http://svn.code.sf.net/p/rkward/code/trunk/rkward'
        for ver in ['0.5.7', '0.6.0']:
            self.targets[ver] = 'http://downloads.sourceforge.net/rkward/rkward-' + ver + '.tar.gz'
            self.targetInstSrc[ ver] = 'rkward-' + ver
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies[ 'testing/r-base' ] = 'default'
        self.dependencies[ 'kde/kate' ] = 'default'  # provides katepart

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        r_executable = os.path.join( self.mergeDestinationDir(), "lib", "R", "bin", "R.exe" )
        self.subinfo.options.configure.defines = " -DR_EXECUTABLE=" + r_executable.replace( "\\\\", "/" )

if __name__ == '__main__':
    Package().execute()

