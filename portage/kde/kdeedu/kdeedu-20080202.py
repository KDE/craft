import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdeedu'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['kde/kdebase-runtime'] = 'default'

        self.buildDependencies['kdesupport/eigen2'] = 'default'
        self.dependencies['win32libs-bin/cfitsio'] = 'default'
        self.dependencies['win32libs-bin/libnova'] = 'default'
        self.dependencies['win32libs-bin/openbabel'] = 'default'
        self.dependencies['win32libs-bin/boost'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF"

if __name__ == '__main__':
    Package().execute()
