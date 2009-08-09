# -*- coding: utf-8 -*-
import info

from Package.CMakePackageBase import *
        
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "trunk/KDE/kdesdk#norecursive;trunk/KDE/kdesdk/umbrello;trunk/KDE/kdesdk/cmake"
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kdesupport/oxygen-icons'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.onlyBuildTargets = 'umbrello' 
            
if __name__ == '__main__':
    Package().execute()

    
