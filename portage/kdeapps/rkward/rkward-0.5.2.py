import info
import os

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'svnHEAD' ] = 'http://rkward.svn.sourceforge.net/svnroot/rkward/trunk/rkward'
        # no "release" targets defined, yet. Releases up to RKWard 0.5.2 (current) had an additional dependency on PHP, which we do not provide
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies[ 'testing/r-base' ] = 'default'
        self.dependencies[ 'virtual/kdebase-runtime' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
	def __init__( self ):
		self.subinfo = subinfo()
		CMakePackageBase.__init__( self )
        r_executable = os.path.join( self.mergeDestinationDir(), "lib", "R", "bin", "R.exe" )
        self.subinfo.options.configure.defines = " -DR_EXECUTABLE=" + r_executable.replace( "\\\\", "/" )

if __name__ == '__main__':
	Package().execute()

