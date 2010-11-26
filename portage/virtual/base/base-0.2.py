import info
import os
import emergePlatform
import compiler
from Package.VirtualPackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.2'] = ""
        self.defaultTarget = '0.2'
        
    def setDependencies( self ):
        if not os.getenv('EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES'):
            self.buildDependencies['gnuwin32/wget']       = 'default'
            self.buildDependencies['dev-util/7zip']       = 'default'
            self.buildDependencies['gnuwin32/patch']      = 'default'
            self.buildDependencies['gnuwin32/sed']        = 'default'
            self.buildDependencies['dev-util/cmake']      = 'default'
            self.buildDependencies['dev-util/subversion'] = 'default'
            self.buildDependencies['dev-util/git']        = 'default'
            
        # for creating combined packages
        self.buildDependencies['dev-util/pexports']   = 'default'
        
        #add c++ runtime if we xcompile
        if emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs-bin/runtime-ce']   = 'default'

        if not os.getenv('EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES'):
            if os.getenv( "SVN_SSH" ) == "plink" or \
                    os.getenv( "GIT_SSH" ) == "plink":
                self.buildDependencies['dev-util/putty']      = 'default'

            if os.getenv( "KDECOMPILER" ) == "mingw4":
                if emergePlatform.buildArchitecture() == 'x64':
                    self.buildDependencies['dev-util/mingw-w64']    = 'default'
                elif emergePlatform.buildArchitecture() == 'arm-wince':
                    self.buildDependencies['dev-util/cegcc-arm-wince'] = 'default'
                else:
                    if compiler.isMinGW32():
                        self.buildDependencies['dev-util/mingw4']    = 'default'
                    else:
                        self.buildDependencies['dev-util/mingw-w32']    = 'default'
            if (os.getenv( "KDECOMPILER" ) == "msvc2008" or os.getenv( "KDECOMPILER" ) == "msvc2005" or os.getenv( "KDECOMPILER" ) == "msvc2010") and os.getenv( "EMERGE_MAKE_PROGRAM" ) != "":
                self.buildDependencies['dev-util/jom']        = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
