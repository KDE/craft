# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):       
        self.svnTargets['gitHEAD'] = "[git]git://gitorious.org/qt/qtdeclarative.git|dev"

        self.defaultTarget = "gitHEAD"

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtxmlpatterns'] = 'default'
        self.dependencies['libs/qtsvg'] = 'default'
        self.dependencies['libs/qtjsbackend'] ='default'


from Package.Qt5CorePackageBase import *

class Package( Qt5CorePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        Qt5CorePackageBase.__init__( self )
        
if __name__ == '__main__':
    Package().execute()
