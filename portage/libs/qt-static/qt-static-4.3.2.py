# -*- coding: utf-8 -*-
import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = "http://www.winkde.org/pub/kde/ports/win32/repository/other"
        self.targets[ '4.3.2' ] = self.getPackage( repoUrl, "qt-static", '4.3.2', '.zip' )
        for version in ['4.5.1-1']:
            self.targets[ version ] = self.getPackage( repoUrl, "qt-static", version)
        self.defaultTarget = '4.5.1-1'
    
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
