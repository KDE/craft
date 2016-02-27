import os
import subprocess
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
            self.r_dir = os.path.join( self.mergeDestinationDir(), "lib", "R", "bin", "x64" )
        else:
            self.r_dir = os.path.join( self.mergeDestinationDir(), "lib", "R", "bin", "i386" )
        self.subinfo.options.configure.defines = " -DR_EXECUTABLE=" + os.path.join (self.r_dir, "R.exe").replace( "\\\\", "/" )
        if compiler.isMSVC():
            self.realconfigure = self.configure
            self.configure = self.msvcconfigure

    def msvcconfigure( self ):
        # Need to create a .lib-file for R.dll, first
        dump = subprocess.check_output(["dumpbin", "/exports", os.path.join(self.r_dir, "R.dll")]).decode("latin1").splitlines ()
        exports = []
        for line in dump:
            fields = line.split ()
            if len (fields) != 4:
                continue
            exports.append(fields[3])
        self.enterBuildDir()
        deffile = open(os.path.join(self.buildDir(), "R.def"), 'w')
        deffile.write("EXPORTS\r\n")
        deffile.write("\r\n".join(exports) + "\r\n")
        deffile.close()
        subprocess.call(["lib", "/def:R.def", "/out:R.lib", "/machine:x86"])

        # Now configure as usual.
        return self.realconfigure()

