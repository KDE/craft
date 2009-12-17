# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdepim'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdepim'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdepim'
        self.defaultTarget = '20091201'

    def setDependencies( self ):
        self.hardDependencies['enterprise5/kdepimlibs-e5'] = 'default'
        self.hardDependencies['enterprise5/kdebase-runtime-e5'] = 'default'
        self.hardDependencies['enterprise5/grantlee-e5'] = 'default'
        self.hardDependencies['win32libs-bin/sqlite'] = 'default'
        
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DKLEO_SYNCHRONOUS_API_HOTFIX=ON"
        #        self.subinfo.options.configure.defines += " -DBUILD_doc=OFF"

if __name__ == '__main__':
    Package().execute()

