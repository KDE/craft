import base
import info

SRC_URI= "http://downloads.activestate.com/ActivePerl/Windows/5.8/ActivePerl-5.8.8.822-MSWin32-x86-280952.zip"

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['5.8.8'] = SRC_URI
        self.targetInstSrc['5.8.8'] = "ActivePerl-5.8.8.822-MSWin32-x86-280952\\perl"
        self.defaultTarget = '5.8.8'
        
class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, SRC_URI )
    self.subinfo = subinfo()
    if self.traditional:
        self.instdestdir = "perl"
		
if __name__ == '__main__':
    subclass().execute()
