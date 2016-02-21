import os

import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] =  '[git]kde:rkward|frameworks'
        for ver in ['0.6.4']:
            self.targets[ver] = 'http://download.kde.org/stable/rkward/' + ver + '/rkward-' + ver + '.tar.gz'
            self.targetInstSrc[ ver] = 'rkward-' + ver
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies[ 'testing/r-base' ] = 'default'
        if self.buildTarget in ['0.6.4', '0.6.5']:
            # Hm, will this still work at all? kate port does not seem to provide KDE 4 version, anymore
            self.dependencies[ 'kde/kate' ] = 'default'  # provides katepart
        else:
            self.dependencies["frameworks/ki18n"] = "default"
            self.dependencies["frameworks/ktexteditor"] = "default"
            self.dependencies["frameworks/kwindowsystem"] = "default"
            self.dependencies["frameworks/kdewebkit"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        if compiler.isX64():
            r_executable = os.path.join( self.mergeDestinationDir(), "lib", "R", "bin", "x64", "R.exe" )
        else:
            r_executable = os.path.join( self.mergeDestinationDir(), "lib", "R", "bin", "i386", "R.exe" )
        self.subinfo.options.configure.defines = " -DR_EXECUTABLE=" + r_executable.replace( "\\\\", "/" )


