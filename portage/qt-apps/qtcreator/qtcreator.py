# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):       
        self.svnTargets[ "gitHEAD" ] = "git://gitorious.org/qt-creator/qt-creator.git"
        self.targets[ "3.1.1" ] = "http://download.qt-project.org/official_releases/qtcreator/3.1/3.1.1/qt-creator-opensource-src-3.1.1.tar.gz"
        self.targetDigests['3.1.1'] = '95e0842447afb91259b0ead2fba7599821767001'
        self.targetInstSrc[ "3.1.1" ] = "qt-creator-opensource-src-3.1.1"
        self.defaultTarget = "3.1.1"

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'


from Package.Qt5CorePackageBase import *

class Package( Qt5CorePackageBase ):
    def __init__( self, **args ):
        Qt5CorePackageBase.__init__( self )

