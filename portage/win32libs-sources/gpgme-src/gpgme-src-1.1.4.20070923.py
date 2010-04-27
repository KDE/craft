# -*- coding: iso-8859-15 -*-
import base
import os
import shutil
import utils
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.3.0'] = 'ftp://ftp.gnupg.org/gcrypt/gpgme/gpgme-1.3.0.tar.bz2'
        self.targetInstSrc['1.3.0'] = 'gpgme-1.3.0'
        self.defaultTarget = '1.3.0'
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
        
        #self.buildInSource=True
        
        compiler = self.compiler()
        if self.buildArchitecture()=="x64" and compiler == "mingw4":
            compiler="mingw64"
        elif(compiler == "mingw4"):
            compiler="mingw"
        else:
            utils.die("msvc is not supported");
            

if __name__ == '__main__':
     Package().execute()
