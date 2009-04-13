import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.8.6'] = "ftp://ftp.ruby-lang.org/pub/ruby/binaries/mswin32/ruby-1.8.6-i386-mswin32.zip"
        self.defaultTarget = '1.8.6'
    
class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.subinfo = subinfo()

  def unpack(self):
    res = base.baseclass.unpack( self )
    # ruby package contains a file called MANIFEST that we need to get
    # out of the way so we can make the manifest dir
    if res:
      os.remove( os.path.join( self.workdir, self.instsrcdir, "MANIFEST" ) )
    return res

if __name__ == '__main__':
    subclass().execute()
