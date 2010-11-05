import base
import info
import os
import platform
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.2'] = ""
        self.defaultTarget = '0.2'
        
    def setDependencies( self ):
        if not os.getenv('EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES'):
            self.hardDependencies['gnuwin32/wget']       = 'default'
            self.hardDependencies['dev-util/7zip']       = 'default'
            self.hardDependencies['gnuwin32/patch']      = 'default'
            self.hardDependencies['gnuwin32/sed']        = 'default'
            self.hardDependencies['dev-util/cmake']      = 'default'
            self.hardDependencies['dev-util/subversion'] = 'default'
            self.hardDependencies['dev-util/git']        = 'default'
            
        # for creating combined packages
        self.hardDependencies['dev-util/pexports']   = 'default'
        
        #add c++ runtime if we xcompile
        if platform.isCrossCompilingEnabled():
            self.hardDependencies['win32libs-bin/runtime-ce']   = 'default'

        if not os.getenv('EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES'):
            if os.getenv( "SVN_SSH" ) == "plink" or \
                    os.getenv( "GIT_SSH" ) == "plink":
                self.hardDependencies['dev-util/putty']      = 'default'

            if os.getenv( "KDECOMPILER" ) == "mingw4":
                if platform.buildArchitecture() == 'x64':
                    self.hardDependencies['dev-util/mingw-w64']    = 'default'
                elif platform.buildArchitecture() == 'arm-wince':
                    self.hardDependencies['dev-util/cegcc-arm-wince'] = 'default'
                else:
                    if compiler. isMinGW32():
                        self.hardDependencies['dev-util/mingw4']    = 'default'
                    else:
                        self.hardDependencies['dev-util/mingw-w32']    = 'default'
            if (os.getenv( "KDECOMPILER" ) == "msvc2008" or os.getenv( "KDECOMPILER" ) == "msvc2005" or os.getenv( "KDECOMPILER" ) == "msvc2010") and os.getenv( "EMERGE_MAKE_PROGRAM" ) != "":
                self.hardDependencies['dev-util/jom']        = 'default'
                
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True              

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
