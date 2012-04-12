# -*- coding: utf-8 -*-
import compiler
import info
import portage
import shutil


class subinfo(info.infoclass):
    def setTargets( self ):       
        self.svnTargets['gitHEAD'] = "[git]git://gitorious.org/qt/qtsvg.git" 

        self.defaultTarget = "gitHEAD"

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'


from Package.Qt5CoreBuildSystem import *

class Package( Qt5CoreBuildSystem ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        Qt5CoreBuildSystem.__init__( self )        
       

        
if __name__ == '__main__':
    Package().execute()
