import base
import os
import info

SRC_URI= "http://www.winkde.org/pub/kde/ports/win32/repository/other/upx-3.0.3-bin.zip"

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.0.3'] = SRC_URI
        self.defaultTarget = '3.0.3'
    
class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, SRC_URI )
    if self.traditional:
        self.instdestdir = "upx"
    self.subinfo = subinfo()

  def unpack(self):
    res = base.baseclass.unpack( self )
    return res

if __name__ == '__main__':
    subclass().execute()
