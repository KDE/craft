# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        """ """
        self.svnTargets['svnHEAD'] = "git://qt.gitorious.org/qt-labs/jom.git"
        self.svnTargets['mingw'] = "git://gitorious.org/~saroengels/qt-labs/jom-mingw.git"
        self.svnTargets['cmake'] = "git://gitorious.org/~saroengels/qt-labs/jom-cmake.git"
        self.svnTargets['static'] = "git://qt.gitorious.org/qt-labs/jom.git"
        self.targetSrcSuffix['cmake'] = "cmake"
        self.targetSrcSuffix['mingw'] = "mingw"
        
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['testing/libantlr'] = 'default'
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DJOM_ENABLE_TESTS=ON"

if __name__ == '__main__':
    Package().execute()
