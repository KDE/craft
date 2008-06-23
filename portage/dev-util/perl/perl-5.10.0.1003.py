import base
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['5.8.8'] = "http://downloads.activestate.com/ActivePerl/Windows/5.8/ActivePerl-5.8.8.822-MSWin32-x86-280952.zip"
        self.targets['5.10.0'] = "http://downloads.activestate.com/ActivePerl/Windows/5.10/ActivePerl-5.10.0.1003-MSWin32-x86-285500.zip"
        self.targetInstSrc['5.8.8'] = "ActivePerl-5.8.8.822-MSWin32-x86-280952\\perl"
        self.targetInstSrc['5.10.0'] = "ActivePerl-5.10.0.1003-MSWin32-x86-285500\\perl"
        self.defaultTarget = '5.10.0'
        
class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.subinfo = subinfo()
		
if __name__ == '__main__':
    subclass().execute()
