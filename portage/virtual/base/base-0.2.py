import base
import info
import os

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.2'] = ""
        self.defaultTarget = '0.2'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget']       = 'default'
        self.hardDependencies['dev-util/7zip']       = 'default'
        self.hardDependencies['gnuwin32/patch']      = 'default'
        self.hardDependencies['gnuwin32/sed']        = 'default'
        self.hardDependencies['dev-util/cmake']      = 'default'
        self.hardDependencies['dev-util/subversion'] = 'default'
        self.hardDependencies['dev-util/git']        = 'default'
        # for creating combined packages
        self.hardDependencies['dev-util/pexports']   = 'default'

        if os.getenv( "KDECOMPILER" ) == "mingw4":
            if os.getenv("EMERGE_ARCHITECTURE") == 'x64':
                self.hardDependencies['dev-util/mingw-w64']    = 'default'
            elif os.getenv("EMERGE_ARCHITECTURE") == 'arm-wince':
                self.hardDependencies['dev-util/cegcc-arm-wince'] = 'default'
            else:
                self.hardDependencies['dev-util/mingw4']    = 'default'
                
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True              

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
