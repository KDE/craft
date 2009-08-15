# -*- coding: iso-8859-15 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHead'] = 'https://svn.kde.org/home/kde/branches/work/soc-umbrello'
        self.defaultTarget = 'svnHead'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['win32libs-bin/boost'] = 'default'
        self.hardDependencies['win32libs-bin/zip'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        
if __name__ == '__main__':
    Package().execute()
