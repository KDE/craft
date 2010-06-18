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
        self.targets['3.0-pre1'] = "http://samba.org/ftp/ccache/ccache-3.0pre1.tar.bz2"
        self.targetInstSrc['3.0-pre1'] = "ccache-3.0pre1"
        self.targetSrcSuffix['gitHEAD'] = 'git'
        self.defaultTarget = '2.4'
        

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
        self.subinfo.options.package.withCompiler = False
        
    def configure( self ):
        if self.buildTarget in ['gitHEAD', '3.0-pre1']:
            if self.buildTarget in ['gitHEAD']:
              self.subinfo.options.configure.bootstrap = True
            return AutoToolsBuildSystem.configure( self )
        return True

if __name__ == '__main__':
    Package().execute()
