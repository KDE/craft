# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtdeclarative'] = 'default'


from Package.Qt5CorePackageBase import *

class Package( Qt5CorePackageBase ):
    def __init__( self, **args ):
        Qt5CorePackageBase.__init__( self )
