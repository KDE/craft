# -*- coding: utf-8 -*-
import base
import os
import utils
import info
import sys

class subinfo(info.infoclass):
    def setTargets( self ):
        """ """
        self.svnTargets['svnHEAD'] = "git://qt.gitorious.org/qt-labs/jom.git"
        self.svnTargets['static'] = "git://qt.gitorious.org/qt-labs/jom.git"
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['dev-util/msys'] = 'default'
        self.hardDependencies['dev-util/git'] = 'default'
        self.hardDependencies['testing/libantlr'] = 'default'
        pass

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        if self.buildTarget == "static":
            self.buildType = "Release"

        self.createCombinedPackage = True

    def compile( self ):
        if self.buildTarget == "static":
            self.kdeCustomDefines += " -DQT_QMAKE_EXECUTABLE:FILEPATH=%s " % \
            os.path.join(self.rootdir, "qt-static", "bin", "qmake.exe").replace('\\', '/')
        else:
            self.kdeCustomDefines = "-DJOM_ENABLE_TESTS=ON"

        self.kde.sourcePath = self.svndir
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def unittest( self ):
        return self.kdeTest()

    def make_package( self ):
        self.kde.sourcePath = self.svndir
        self.doPackaging("jom")
        return True

if __name__ == '__main__':
    subclass().execute()
