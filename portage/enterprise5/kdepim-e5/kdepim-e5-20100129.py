# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdepim'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdepim'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdepim'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/kdepim'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdepim'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdepim'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdepim'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/kdepim'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdepim'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdepim'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdepim'
        self.defaultTarget = '20100129'

    def setDependencies( self ):
        self.hardDependencies['enterprise5/kdepimlibs-e5'] = 'default'
        self.hardDependencies['enterprise5/kdebase-runtime-e5'] = 'default'
        self.hardDependencies['contributed/libassuan-src'] = 'default'
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

