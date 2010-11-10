# -*- coding: iso-8859-15 -*-
import base
import os
import shutil
import utils
import info
from shells import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.18.1.1'] = 'http://ftp.gnu.org/pub/gnu/gettext/gettext-0.18.1.1.tar.gz'
        self.targetDigests['0.18.1.1'] = '5009deb02f67fc3c59c8ce6b82408d1d35d4e38f'
        self.targetInstSrc['0.18.1.1'] = 'gettext-0.18.1.1'
        self.defaultTarget = '0.18.1.1'
        
    def setDependencies( self ):
        self.hardDependencies['dev-util/perl'] = 'default' # buildtime dependency
        self.hardDependencies['dev-util/msys'] = 'default' # buildtime dependency
        self.hardDependencies['win32libs-bin/win_iconv'] = 'default'


from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.KDEWinPackager import *;

class Package( PackageBase, MultiSource, AutoToolsBuildSystem, KDEWinPackager):
    def __init__( self ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        AutoToolsBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)
        self.subinfo.options.configure.defines = "--disable-java --disable-csharp --disable-shared --enable-static --with-gettext-tools "
        self.subinfo.options.package.withCompiler = None
        self.subinfo.options.package.packageName = 'gettext-tools'


if __name__ == '__main__':
     Package().execute()
