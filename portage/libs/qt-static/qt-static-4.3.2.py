import base
import os
import info

SRC_URI= """
http://www.winkde.org/pub/kde/ports/win32/repository/other/qt-static-msvc-4.3.2-bin.zip
http://www.winkde.org/pub/kde/ports/win32/repository/other/qt-static-msvc-4.3.2-lib.zip
http://www.winkde.org/pub/kde/ports/win32/repository/other/qt-static-msvc-4.3.2-doc.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.3.2'] = SRC_URI
        self.defaultTarget = '4.3.2'
    
class subclass(base.baseclass):
  def __init__(self, **args):
    base.baseclass.__init__( self, args=args )
    self.instdestdir = "qt-static"
    self.subinfo = subinfo()

  def unpack(self):
    res = base.baseclass.unpack( self )
    return res

if __name__ == '__main__':
    subclass().execute()
