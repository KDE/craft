# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets( self ):       
        self.svnTargets['gitHEAD'] = "[git]git://gitorious.org/qt/qtxmlpatterns.git|stable" 

        self.defaultTarget = "gitHEAD"

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'


from Package.Qt5CorePackageBase import *

class Package( Qt5CorePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        Qt5CorePackageBase.__init__( self )        
       

        
if __name__ == '__main__':
    Package().execute()
