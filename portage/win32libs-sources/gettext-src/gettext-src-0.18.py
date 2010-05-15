# -*- coding: iso-8859-15 -*-
import base
import os
import shutil
import utils
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.18'] = 'http://ftp.gnu.org/pub/gnu/gettext/gettext-0.18.tar.gz'
        self.targetDigests['0.18'] = 'de396ec6877a451427d8597197d18c2d4b8f1a26'
        self.targetInstSrc['0.18'] = 'gettext-0.18\\gettext-runtime'
        self.defaultTarget = '0.18'
        
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
        self.buildInSource=True
        self.subinfo.options.configure.defines = "--disable-java  --enable-static=no"
        

        

        if not self.buildArchitecture()=="x64" and compiler == "mingw4":
            utils.die("msvc is not supported");


if __name__ == '__main__':
     Package().execute()
