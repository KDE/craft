# -*- coding: iso-8859-15 -*-
import base
import os
import shutil
import utils
import info

PACKAGE_DLL_NAMES     = """
libaspell-15
libpspell-15
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.60.6'] = 'ftp://ftp.gnu.org/gnu/aspell/aspell-0.60.6.tar.gz'
        self.targetInstSrc['0.60.6'] = 'aspell-0.60.6'
        self.defaultTarget = '0.60.6'
    def setDependencies( self ):
        self.hardDependencies['dev-util/perl'] = 'default' # buildtime dependency
        self.hardDependencies['dev-util/msys'] = 'default' # buildtime dependency
        self.hardDependencies['win32libs-bin/iconv'] = 'default'


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
        
        compiler = self.compiler()
        if os.getenv("EMERGE_ARCHITECTURE")=="x64" and compiler == "mingw4":
            compiler="mingw64"
        elif(compiler == "mingw4"):
            compiler="mingw"
        else:
            utils.die("msvc is not supported");
            
    def unpack( self ):
        if( not MultiSource.unpack( self ) ):
          return False
        utils.applyPatch( self.sourceDir(), os.path.join( self.packageDir(), "aspell-0.60.6.diff" ), 0 )
        utils.applyPatch( self.sourceDir(), os.path.join( self.packageDir(), "aspell-kde-dirs.diff"),0 )
        return True
        
    def createPackage( self ): 
       for libs in PACKAGE_DLL_NAMES.split():
         self.stripLibs( libs )
       for libs in PACKAGE_DLL_NAMES.split():
         self.createImportLibs( libs )
       return KDEWinPackager.createPackage( self )

if __name__ == '__main__':
     Package().execute()
