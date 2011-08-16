# -*- coding: utf-8 -*-
import info
import os

os.putenv("CXX","g++")
os.putenv("CC","gcc")

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://git.samba.org/ccache.git"
        self.svnTargets['working'] = "git://git.samba.org/ccache.git||206b0c182b8fbe1e115039507c4356ee1316a7fa"
        self.defaultTarget = 'working'


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/autotools'] = 'default'


from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.package.withCompiler = False

if __name__ == '__main__':
    Package().execute()
