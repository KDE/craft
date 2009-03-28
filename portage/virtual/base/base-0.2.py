import base
import info
import os

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.2'] = ""
        self.defaultTarget = '0.2'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget']       = 'default'
        self.hardDependencies['gnuwin32/patch']      = 'default'
        self.hardDependencies['gnuwin32/sed']        = 'default'
        self.hardDependencies['dev-util/cmake']      = 'default'
        self.hardDependencies['dev-util/perl']       = 'default'
        self.hardDependencies['dev-util/subversion'] = 'default'
        if os.getenv( "KDECOMPILER" ) == "mingw":
          self.hardDependencies['dev-util/mingw']    = 'default'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
