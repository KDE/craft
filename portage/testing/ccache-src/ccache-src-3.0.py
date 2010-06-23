# -*- coding: utf-8 -*-
import info
import os

from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.MultiPackager import *
from Package.PackageBase import *


os.putenv("EMERGE_USE_CCACHE","False")


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://git.samba.org/ccache.git"
        self.targetSrcSuffix['gitHEAD'] = 'git'
        self.svnTargets['win_branch'] = "git://gitorious.org/ccache-win/ccache-win.git|windows"
        self.targetSrcSuffix['win_branch'] = 'git-win'
        self.defaultTarget = 'win_branch'
        

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['testing/autotools'] = 'default'
        
class Package(PackageBase, MultiSource, AutoToolsBuildSystem, MultiPackager):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        AutoToolsBuildSystem.__init__(self)        
        MultiPackager.__init__(self)
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.configure.bootstrap = True
        self.subinfo.options.configure.defines = " --enable-dev "

if __name__ == '__main__':
    Package().execute()
