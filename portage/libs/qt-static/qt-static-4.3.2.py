# -*- coding: utf-8 -*-
import base
import os
import info

SRC_URI= """
http://www.winkde.org/pub/kde/ports/win32/repository/other/qt-static-msvc-4.3.2-bin.zip
http://www.winkde.org/pub/kde/ports/win32/repository/other/qt-static-msvc-4.3.2-lib.zip
http://www.winkde.org/pub/kde/ports/win32/repository/other/qt-static-msvc-4.3.2-doc.zip
"""

SRC_URI2 = """
http://www.winkde.org/pub/kde/ports/win32/repository/other/qt-static-msvc-4.5.1-1-bin.tar.bz2
http://www.winkde.org/pub/kde/ports/win32/repository/other/qt-static-msvc-4.5.1-1-lib.tar.bz2
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.3.2'] = SRC_URI
        self.targets['4.5.1'] = SRC_URI2
        self.defaultTarget = '4.5.1'
    
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
