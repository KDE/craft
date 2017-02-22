# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        # HACK
        self.svnTargets[ '5.6' ] = '[git]https://codereview.qt-project.org/qt/qtremoteobjects|5.9' # compatible with 5.6

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'


from Package.Qt5CorePackageBase import *

class Package( Qt5CorePackageBase ):
    def __init__( self, **args ):
        Qt5CorePackageBase.__init__( self )
