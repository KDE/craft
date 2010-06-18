# -*- coding: utf-8 -*-
import info

from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.MultiPackager import *
from Package.PackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['2.4'] = "http://ccache-win32.googlecode.com/svn/trunk/ccache-win32"
        self.svnTargets['gitHEAD'] = "git://git.samba.org/ccache.git"
        self.targetSrcSuffix['gitHEAD'] = 'git'
        self.defaultTarget = '2.4'
        self.options.package.withCompiler = False

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        
class Package(PackageBase, MultiSource, AutoToolsBuildSystem, MultiPackager):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        AutoToolsBuildSystem.__init__(self)        
        MultiPackager.__init__(self)
        self.buildInSource = True
        
    def configure( self ):
        return True

if __name__ == '__main__':
    Package().execute()
