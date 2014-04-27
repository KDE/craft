# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'https://github.com/libgit2/libgit2.git'


        self.shortDescription = "a portable C library for accessing git repositories"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )
#        self.subinfo.options.configure.defines = "-DDBUS_REPLACE_LOCAL_DIR=ON "

if __name__ == '__main__':
    Package().execute()
