# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        """ """
        self.svnTargets['svnHEAD'] = "git://qt.gitorious.org/qt-labs/jom.git"
        self.svnTargets['mingw'] = "git://gitorious.org/~saroengels/qt-labs/jom-mingw.git"
        self.svnTargets['cmake'] = "git://gitorious.org/~saroengels/qt-labs/jom-cmake.git"
        self.svnTargets['static'] = "git://qt.gitorious.org/qt-labs/jom.git"
        self.svnTargets['static-cmake'] = "git://gitorious.org/~saroengels/qt-labs/jom-cmake.git"
        self.targetSrcSuffix['cmake'] = "cmake"
        self.targetSrcSuffix['mingw'] = "mingw"
        
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/msys'] = 'default'  # for flex
        self.buildDependencies['dev-util/qlalr'] = 'default'
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DFLEX_EXECUTABLE=" + os.path.join( os.getenv( "KDEROOT" ), "msys", "bin", "flex.exe" ) + " -DJOM_ENABLE_TESTS=ON"
        if self.buildTarget.startswith( "static" ):
            self.subinfo.options.configure.defines += " -DQT_QMAKE_EXECUTABLE=" + os.path.join( os.getenv( "KDEROOT" ), "qt-static", "bin", "qmake.exe" )

if __name__ == '__main__':
    Package().execute()
