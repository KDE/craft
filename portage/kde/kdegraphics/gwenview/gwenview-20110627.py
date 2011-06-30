import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:gwenview|KDE/4.6|'
        self.shortDescription = "Image viewer for KDE"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kde/kde-baseapps'] = 'default'
        self.dependencies['kde/libkipi'] = 'default' 
        self.dependencies['win32libs-bin/exiv2'] = 'default'
        self.dependencies['win32libs-bin/jpeg'] = 'default'
   


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
