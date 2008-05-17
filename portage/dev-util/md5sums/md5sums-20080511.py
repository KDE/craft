import base
import os
import info

SRC_URI = "http://www.winkde.org/pub/kde/ports/win32/repository/other/md5sums-20080511-bin.zip"

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['20080511'] = SRC_URI
        self.defaultTarget = '20080511'
    
class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, SRC_URI )
    if self.traditional:
        self.instdestdir = "md5sums"
    self.subinfo = subinfo()

  def unpack(self):
    res = base.baseclass.unpack( self )
    return res

if __name__ == '__main__':
    subclass().execute()
