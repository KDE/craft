 # -*- coding: utf-8 -*-
import info
import os
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "svn://svn.code.sf.net/p/cmusphinx/code/trunk/SphinxTrain"
        self.patchToApply['svnHEAD'] = ('sphinxtrain-no-configure.diff', 0)
        self.defaultTarget = 'svnHEAD'


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['testing/sphinxbase'] = 'default'
        if compiler.isMinGW():
            self.buildDependencies['dev-util/autotools'] = 'default'


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *

class PackageMinGW(AutoToolsPackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.defines = " --with-sphinxbase-build=/r/build/testing/sphinxbase-0.8-20121205/work/mingw4-RelWithDebInfo-svnHEAD --with-sphinxbase=/r/download/svn-src/sphinxbase "


    def configure( self):
        return AutoToolsPackageBase.configure( self, cflags="-std=c99 -I/r/include/mingw", ldflags="")
        

if compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__( self ):
            PackageMinGW.__init__( self )
else:
    class Package(VirtualPackageBase):
        def __init__( self ):
            self.subinfo = subinfo()
            VirtualPackageBase.__init__( self )

if __name__ == '__main__':
      Package().execute()
