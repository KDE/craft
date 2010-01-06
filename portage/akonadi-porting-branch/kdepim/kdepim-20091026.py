# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svn'] = 'branches/work/akonadi-ports/kdepim'
        self.defaultTarget = 'svn'

    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['akonadi-porting-branch/kdepimlibs'] = 'default'
        self.hardDependencies['win32libs-bin/sqlite'] = 'default'
        self.hardDependencies['akonadi-porting-branch/grantlee'] = 'default'
        self.hardDependencies['contributed/libassuan-src'] = 'default'
        
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DKLEO_SYNCHRONOUS_API_HOTFIX=ON"
        #        self.subinfo.options.configure.defines += " -DBUILD_doc=OFF"

if __name__ == '__main__':
    Package().execute()

